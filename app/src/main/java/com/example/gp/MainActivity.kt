package com.example.gp

import android.content.Context
import android.content.Intent
import android.content.SharedPreferences
import android.os.Bundle
import android.widget.Button
import android.widget.EditText
import android.widget.Toast
import androidx.appcompat.app.AppCompatActivity
import com.android.volley.NetworkResponse
import com.android.volley.ParseError
import com.android.volley.Request
import com.android.volley.Response
import com.android.volley.toolbox.JsonObjectRequest
import com.android.volley.toolbox.Volley
import okhttp3.Cookie
import org.json.JSONObject
import java.io.UnsupportedEncodingException


class MainActivity : AppCompatActivity() {
    private val Sign_RequestCode = 1
    private lateinit var login: Button
    private lateinit var name: EditText
    private lateinit var psw: EditText
    private var _name: String? = null
    private var _psw: String? = null
    var sharedPreferences :SharedPreferences = getSharedPreferences("prefs", Context.MODE_PRIVATE)
    val editor = sharedPreferences.edit()

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_main)
        val queue = Volley.newRequestQueue(this)
        login = findViewById(R.id.login)
        name = findViewById(R.id.name)
        psw = findViewById(R.id.psw)

        login.setOnClickListener {
            val inputName = name.text.toString()
            val inputPsw = psw.text.toString()
            val LoginRequest = JSONObject()
            LoginRequest.accumulate("username", inputName)
            LoginRequest.accumulate("password", inputPsw)
            val jsonObjectRequest = JsonObjectRequest(
                Request.Method.POST, "http://127.0.0.1:8000/api/login", LoginRequest,
                { response ->
                    Toast.makeText(this, response.toString(), Toast.LENGTH_SHORT)
                        .show()
                    if (response.has("auth")) {

                        editor.putString("usr", inputName)
                        editor.putString("pwd", inputPsw)
                        editor.apply()
                        Toast.makeText(this, "log successfully", Toast.LENGTH_SHORT).show()
                        val intent = Intent(this, home_page::class.java)
                        intent.putExtra("usr", inputName); intent.putExtra("psw", inputPsw)
                        startActivity(intent)
                        finish()
                    } else {
                        Toast.makeText(this, "wrong username or password", Toast.LENGTH_LONG)
                            .show()
                    }
                },
                { error ->
                    Toast.makeText(this, "network error", Toast.LENGTH_SHORT)
                        .show()
                }
            )

            queue.add(jsonObjectRequest)


        }
    }

    protected fun parseNetworkResponse(response: NetworkResponse){
        val responseHEAD = response.headers
        val rawcookies = responseHEAD!!["Set-Cookie"]
        editor.putString("login_cookie",rawcookies)
        editor.apply()
    }

    override fun onActivityResult(requestCode: Int, resultCode: Int, data: Intent?) {
        super.onActivityResult(requestCode, resultCode, data)
        if (requestCode == Sign_RequestCode && resultCode == RESULT_OK && data != null) {
            _name = data.getStringExtra("name")
            _psw = data.getStringExtra("psw")
        }
    }
}
