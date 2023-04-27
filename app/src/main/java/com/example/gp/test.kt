package com.example.gp

import android.graphics.Bitmap
import android.util.Config
import android.util.Log
import com.android.volley.*
import com.android.volley.toolbox.HttpHeaderParser
import com.android.volley.toolbox.StringRequest
import com.android.volley.toolbox.Volley
import java.io.UnsupportedEncodingException

fun main() {
    val mQueue: RequestQueue = Volley.newRequestQueue(this)
    val stringRequest: StringRequest =
        object : StringRequest(Request.Method.POST, "http://127.0.0.1:8000",
            object : Response.Listener<String?> {
                @Override
                fun onResponse(s: String?) {}
        },
            object : Response.ErrorListener() {
            fun onErrorResponse(volleyError: VolleyError?) {}
        }) {
            @get:Throws(AuthFailureError::class)
            protected val params: Map<String, String>?
                protected get() = HashMap()

            protected fun parseNetworkResponse(response: NetworkResponse): Response<String?>? {
                return try {
                    val responseHeaders: Map<String, String> = response.headers
                    val rawCookies = responseHeaders["Set-Cookie"]
                    saveSettingNote(Config.Cookie, rawCookies) //保存Cookie-saveSettingNote是本地存储
                    Log.i("px", rawCookies + "\n")
                    val dataString = String(response.data, charset("UTF-8"))
                    Log.i("px", dataString)
                    Response.success(dataString, HttpHeaderParser.parseCacheHeaders(response))
                } catch (e: UnsupportedEncodingException) {
                    Response.error(ParseError(e))
                }
            }
        }
    mQueue.add(stringRequest)
}