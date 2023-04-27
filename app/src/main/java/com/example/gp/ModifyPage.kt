package com.example.gp

import android.content.Intent
import androidx.appcompat.app.AppCompatActivity
import android.os.Bundle
import android.widget.Button
import android.widget.EditText
import android.widget.Toast
import com.android.volley.Request
import com.android.volley.toolbox.JsonObjectRequest
import com.android.volley.toolbox.Volley
import org.json.JSONObject
import java.net.URI
import java.net.URL
import java.text.SimpleDateFormat
import java.time.LocalDateTime
import java.time.format.DateTimeFormatter
import java.util.*

class ModifyPage : AppCompatActivity() {
    val queue = Volley.newRequestQueue(this)
    val url_prefix = "http://127.0.0.1:8000/api/cargo/"
    private lateinit var id : EditText
    private lateinit var name : EditText
    private lateinit var weight : EditText
    private lateinit var description : EditText
    private lateinit var save : Button
    private lateinit var back : Button

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_modify_page)
        val queue = Volley.newRequestQueue(this)

        id = findViewById(R.id.modified_id)
        name = findViewById(R.id.modified_name)
        weight = findViewById(R.id.modified_weight)
        description = findViewById(R.id.modified_description)
        save = findViewById(R.id.modified_save)
        back = findViewById(R.id.modified_back)

        val original_id = getIntent().getStringExtra("id"); id.setText(original_id)
        val original_name = getIntent().getStringExtra("name"); name.setText(original_name)
        val original_weight = getIntent().getStringExtra("weight"); weight.setText(original_weight)
        val original_desc = getIntent().getStringExtra("description"); description.setText(original_desc)
        val username = getIntent().getStringExtra("usr"); val password = getIntent().getStringExtra("usr")

        val LoginRequest = JSONObject()
        LoginRequest.accumulate("username",username)
        LoginRequest.accumulate("password",password)
        val jsonObjectRequest = JsonObjectRequest(
            Request.Method.POST,"http://127.0.0.1:8000/api/login",LoginRequest,
            { response ->
                Toast.makeText(this, "Account verified", Toast.LENGTH_SHORT)
                    .show()
            },
            {error ->
                Toast.makeText(this, "network error", Toast.LENGTH_SHORT)
                    .show()
            }
        )
        queue.add(jsonObjectRequest)
        save.setOnClickListener {
            val url = url_prefix + id.text
            val savePOST = JSONObject()
            savePOST.accumulate("name",name.text)
            savePOST.accumulate("weight",weight.text)
            savePOST.accumulate("desc",description.text)
            val calendar = Calendar.getInstance()
            val date = calendar.get(Calendar.YEAR).toString() + "-" + calendar.get(Calendar.MONTH) + "-" + calendar.get(Calendar.DATE)
            savePOST.accumulate("arrival_date", date)
            val saveRequest = JsonObjectRequest(
                Request.Method.PUT, url, savePOST,
                { response ->
                    Toast.makeText(this, "Successfully saved", Toast.LENGTH_SHORT)
                        .show()
                },
                { error ->
                    Toast.makeText(this, "Error saving", Toast.LENGTH_SHORT)
                        .show()
                }
            )
            queue.add(saveRequest)
            startActivity(Intent(this,home_page::class.java))
            finish()
        }





    }
}