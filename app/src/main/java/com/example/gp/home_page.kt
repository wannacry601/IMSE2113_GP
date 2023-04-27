package com.example.gp

import android.Manifest
import android.app.Activity
import android.content.Context
import android.content.Intent
import android.content.SharedPreferences
import android.content.pm.PackageManager
import android.media.AudioManager
import android.media.ToneGenerator
import androidx.appcompat.app.AppCompatActivity
import android.os.Bundle
import android.util.Log
import android.view.View
import android.widget.Button
import android.widget.EditText
import android.widget.TextView
import android.widget.Toast
import androidx.activity.result.contract.ActivityResultContracts
import androidx.core.app.ActivityCompat
import androidx.core.content.ContextCompat
import com.android.volley.Request
import com.android.volley.toolbox.JsonObjectRequest
import com.android.volley.toolbox.Volley

class home_page : AppCompatActivity() {
    companion object {
        private const val PERMISSION_CAMERA_REQUEST = 1
    }

    val queue = Volley.newRequestQueue(this)
    private val TAG = "home_page"
    private lateinit var username: EditText
    private lateinit var itemid: EditText
    private lateinit var itemname: EditText
    private lateinit var itemweight: EditText
    private lateinit var itemdescription: EditText
    private lateinit var qrscan: Button
    private lateinit var itemmodify: Button
    private lateinit var itemadd: Button
    private lateinit var logout: Button
    lateinit var sharedPreferences: SharedPreferences

    val startForResult =
        registerForActivityResult(ActivityResultContracts.StartActivityForResult()) {
                result ->
            if (result.resultCode == Activity.RESULT_OK) {
                Log.d(TAG, "Result OK")
                if (result.data?.hasExtra("itemname")!!){
                    val name = result.data!!.extras?.getString("itemname") ?: "Item not found"
                    itemname.setText(name)
                }
                if (result.data?.hasExtra("weight")!!){
                    val weight = result.data!!.extras?.getString("weight") ?: "Item not found"
                    itemweight.setText(weight)
                }
                if (result.data?.hasExtra("description")!!){
                    val description = result.data!!.extras?.getString("description") ?: "Item not found"
                    itemdescription.setText(description)
                }
                if (result.data?.hasExtra("itemid")!!){
                    val description = result.data!!.extras?.getString("item") ?: "Item not found"
                    itemid.setText(description)
                }
            }
            else {
                Log.d(TAG, result.toString())
            }
        }

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_home_page)
        username = findViewById(R.id.username)
        itemid = findViewById(R.id.item_id)
        itemname = findViewById(R.id.item_name)
        itemweight = findViewById(R.id.item_weight)
        itemdescription = findViewById(R.id.item_description)

        var has_scanned = false
        qrscan = findViewById(R.id.scan_qr_code)
        qrscan.setOnClickListener {

            if (isCameraPermissionGranted()) {
                startForResult.launch(Intent(this, QR_Scanner::class.java))
                has_scanned = true
            } else {
                requestPermissionCamera()
            }
        }

        itemmodify = findViewById(R.id.item_modify)
        if (!has_scanned) itemmodify.setEnabled(false)
        itemmodify.setOnClickListener {
            sharedPreferences = getSharedPreferences("prefs", Context.MODE_PRIVATE)
            val username = sharedPreferences.getString("usr",null)!!
            val password = sharedPreferences.getString("pwd",null)!!
            val intent = Intent(this,ModifyPage::class.java)
            intent.putExtra("name",itemname.text)
            intent.putExtra("weight",itemweight.text)
            intent.putExtra("description",itemdescription.text)
            intent.putExtra("id",itemid.text)
            intent.putExtra("usr",username)
            intent.putExtra("pwd",password)
            startActivity(intent)
        }

        itemadd = findViewById(R.id.item_add)
        itemadd.setOnClickListener {

        }

        logout = findViewById(R.id.logout)
        logout.setOnClickListener {
            val logoutRequest = JsonObjectRequest(
                Request.Method.POST, "http://127.0.0.1:8000/api/logout", null,
                { response ->
                    val status = response.get("message")
                    if (status == "Logged out") {
                        val editor = sharedPreferences.edit()
                        editor.clear()
                        editor.apply()
                        val intent = Intent(this,home_page::class.java)
                        startActivity(intent)
                        finish()
                    }
                    else Toast.makeText(this,"Logout error",Toast.LENGTH_SHORT).show()
                },
                { error ->
                    Toast.makeText(this,"Logout error",Toast.LENGTH_SHORT).show()
                }
            )
            queue.add(logoutRequest)
        }




    }
    fun requestPermissionCamera() {
        ActivityCompat.requestPermissions(
            this,
            arrayOf(Manifest.permission.CAMERA),
            PERMISSION_CAMERA_REQUEST
        )
    }

    private fun isCameraPermissionGranted(): Boolean {
        return ContextCompat.checkSelfPermission(
            baseContext,
            Manifest.permission.CAMERA
        ) == PackageManager.PERMISSION_GRANTED
    }




}