package com.example.filmcast

import android.annotation.SuppressLint
import android.content.Intent
import android.os.Bundle
import android.text.InputType
import android.widget.Button
import android.widget.EditText
import android.widget.ImageView
import android.widget.Toast
import androidx.activity.enableEdgeToEdge
import androidx.appcompat.app.AppCompatActivity
import com.google.firebase.FirebaseApp
import com.google.firebase.auth.FirebaseAuth
import okhttp3.Call
import okhttp3.Callback
import okhttp3.MediaType.Companion.toMediaType
import okhttp3.OkHttpClient
import okhttp3.Request
import okhttp3.RequestBody.Companion.toRequestBody
import okhttp3.Response
import okhttp3.ResponseBody.Companion.toResponseBody
import okio.IOException
import org.json.JSONObject

class LoginActivity : AppCompatActivity() {
    @SuppressLint("MissingInflatedId")

    private var passwordVisible = false
    private lateinit var auth: FirebaseAuth

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        enableEdgeToEdge()
        setContentView(R.layout.activity_login)
        FirebaseApp.initializeApp(this)
        auth = FirebaseAuth.getInstance()

        val username = findViewById<EditText>(R.id.et_username)
        val password = findViewById<EditText>(R.id.et_password)
        val loginbtn = findViewById<Button>(R.id.btn_login)
        val registerbtn = findViewById<Button>(R.id.btn_register)
        val togglebtn = findViewById<ImageView>(R.id.passwordVisibilityToggle)

        togglebtn.setOnClickListener{ //boton ocultar/mostrar contraseña
            if (passwordVisible) {
                password.inputType =
                    InputType.TYPE_CLASS_TEXT or InputType.TYPE_TEXT_VARIATION_PASSWORD
            } else {
                password.inputType = InputType.TYPE_CLASS_TEXT or InputType.TYPE_TEXT_VARIATION_VISIBLE_PASSWORD
            }

            password.setSelection(password.text.length)
            passwordVisible = !passwordVisible
        }


        loginbtn.setOnClickListener{

            val emailText = username.text.toString().trim()
            val passwordText = password.text.toString().trim()

            if (emailText.isNotEmpty() && passwordText.isNotEmpty()) {
                iniciarSesion(emailText,passwordText)
            }
            else{
                Toast.makeText(this,"porfavor, ingresa todos los campos.",Toast.LENGTH_SHORT).show()
            }
        }

        registerbtn.setOnClickListener{

            val intent = Intent(this, RegistroActivity::class.java)
            startActivity(intent)

        }

        }

    private fun iniciarSesion(emailText: String, passwordText: String) {
        val url = "aquivaellink.com"

        val json = JSONObject()
        json.put("email",emailText)
        json.put("password",passwordText)

        val mediaType = "application/json; charset=utf-8".toMediaType()
        val body = json.toString().toRequestBody(mediaType)

        val client = OkHttpClient()
        val request = Request.Builder()
            .url(url)
            .post(body)
            .build()

        client.newCall(request).enqueue(object : Callback {
            override fun onFailure(call: Call, e: IOException){
                runOnUiThread{
                    Toast.makeText(this@LoginActivity,"Error ${e.message}", Toast.LENGTH_SHORT).show()
                }
            }

            override fun onResponse(call: Call, response: Response){
                response.body?.toString()?.let {
                    val jsonResponse = JSONObject(it)
                    val success = jsonResponse.getBoolean("success")
                    val message = jsonResponse.getString("message")

                    runOnUiThread {
                        Toast.makeText(this@LoginActivity,message,Toast.LENGTH_SHORT).show()
                        if (success){
                            startActivity(Intent(this@LoginActivity, MenuActivity::class.java))
                            finish()                        }
                    }
                }
            }
        })
    }
}