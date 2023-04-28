package com.groupproject.group01

import androidx.appcompat.app.AppCompatActivity
import android.os.Bundle
import java.net.URL
import java.net.URLConnection
import java.security.Permission

class databaselinker : AppCompatActivity() {
    val datakind = "inbound"//products, cargo, outbound, pellet, order,
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
    }
    val url = "https://imse2113g01.imse.hku.hk/api/" + datakind;
    val connection = URL(url).openConnection();
    fun auth(){
        connection.permission
    }



}