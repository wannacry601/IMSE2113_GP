package com.example.gp


import android.Manifest
import android.content.Intent
import android.content.pm.PackageManager
import android.os.Bundle
import android.os.Handler
import android.os.Looper
import android.util.Log
import android.widget.Toast
import androidx.appcompat.app.AppCompatActivity
import androidx.core.app.ActivityCompat
import com.google.zxing.Result
import org.json.JSONObject
import me.dm7.barcodescanner.zxing.ZXingScannerView

class QR_Scanner : AppCompatActivity(), ZXingScannerView.ResultHandler {
    companion object {
        private const val CAMERA_REQUEST_CODE = 200
    }

    private var mScannerView: ZXingScannerView? = null

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_qr_scanner)

        if (ActivityCompat.checkSelfPermission(this, Manifest.permission.CAMERA) != PackageManager.PERMISSION_GRANTED) {
            ActivityCompat.requestPermissions(this, arrayOf(Manifest.permission.CAMERA), CAMERA_REQUEST_CODE)
        } else {
            startScannerView()
        }
    }

    override fun onResume() {
        super.onResume()

        if (mScannerView == null) {
            startScannerView()
        }

        mScannerView!!.setResultHandler(this)
        mScannerView!!.startCamera()
    }

    override fun onPause() {
        super.onPause()
        mScannerView!!.stopCamera()
    }

    override fun handleResult(result: Result?) {
        Log.v("QRCodeScanner", result!!.text)

        Toast.makeText(this, result.text, Toast.LENGTH_SHORT).show()

        //TODO switch to another activity.
        val jsonpack = JSONObject(result.text);
        val intent = Intent(this,home_page::class.java);
        intent.putExtra("itemid",jsonpack.getString("cargoid"));
        intent.putExtra("itemname",jsonpack.getString("cargo_name"));
        intent.putExtra("weight",jsonpack.getString("weight"));
        intent.putExtra("description",jsonpack.getString("description"));
        startActivity(intent)
    }

    private fun startScannerView() {
        mScannerView = ZXingScannerView(this)
        setContentView(mScannerView)
    }

    override fun onRequestPermissionsResult(requestCode: Int, permissions: Array<out String>, grantResults: IntArray) {
        super.onRequestPermissionsResult(requestCode, permissions, grantResults)

        if (requestCode == CAMERA_REQUEST_CODE) {
            if (grantResults.isNotEmpty() && grantResults[0] == PackageManager.PERMISSION_GRANTED) {
                startScannerView()
            } else {
                Toast.makeText(this, getString(R.string.camera_permission_denied), Toast.LENGTH_SHORT).show()
            }
        }
    }
}
