package com.example.filmcast

import android.annotation.SuppressLint
import android.content.Intent
import android.os.Bundle
import android.text.InputType
import android.widget.Button
import android.widget.EditText
import android.widget.ImageView
import android.widget.Toast
import androidx.appcompat.app.AppCompatActivity
import com.google.firebase.auth.FirebaseAuth
import com.google.firebase.firestore.FirebaseFirestore
import org.json.JSONObject
import okhttp3.*
import okhttp3.MediaType.Companion.toMediaType
import okhttp3.RequestBody.Companion.toRequestBody
import okio.IOException

class RegistroActivity : AppCompatActivity() {
    @SuppressLint("MissingInflatedId", "CutPasteId")

    private var passwordVisible = false
    private lateinit var auth: FirebaseAuth
    private lateinit var firestore: FirebaseFirestore

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_register)
        auth = FirebaseAuth.getInstance()
        firestore = FirebaseFirestore.getInstance()

        val username = findViewById<EditText>(R.id.et_username)
        val email = findViewById<EditText>(R.id.et_email)
        val password = findViewById<EditText>(R.id.et_password)
        val loginbtn = findViewById<Button>(R.id.btn_login)
        val registerbtn = findViewById<Button>(R.id.btn_register)
        val togglebtn = findViewById<ImageView>(R.id.passwordVisibilityToggle)

        //boton para mostrar/esconder contraseña
        togglebtn.setOnClickListener{
            if (passwordVisible) {
                password.inputType =
                    InputType.TYPE_CLASS_TEXT or InputType.TYPE_TEXT_VARIATION_PASSWORD
            } else {
                password.inputType = InputType.TYPE_CLASS_TEXT or InputType.TYPE_TEXT_VARIATION_VISIBLE_PASSWORD
            }

            password.setSelection(password.text.length)
            passwordVisible = !passwordVisible
        }

        //boton para ir al LoginActivity
        loginbtn.setOnClickListener{
            val intent = Intent(this,LoginActivity::class.java)
            startActivity(intent)
        }

        registerbtn.setOnClickListener{
            val usernameText = username.text.toString().trim()
            val emailText = email.text.toString().trim()
            val passwordText = password.text.toString().trim()

            if (usernameText.isNotEmpty() && emailText.isNotEmpty() && passwordText.isNotEmpty()){
                registrarUsuario(usernameText,emailText,passwordText)
            }
            else {
                Toast.makeText(this,"Por favor ingresa todos los campos.", Toast.LENGTH_SHORT).show()
            }

        }


    }

    private fun registrarUsuario(usernameText: String, emailText: String, passwordText: String) {
        val url = "https://model.cuspide.club/nearest-records"

        //crear json con los datos de usuario
        val json =  JSONObject()
        json.put("username",usernameText)
        json.put("email",emailText)
        json.put("password",passwordText)

        //solicitud HTTP POST
        val mediaType = "application/json; charset=utf-8".toMediaType()
        val body = json.toString().toRequestBody(mediaType)

        val client = OkHttpClient()
        val request = Request.Builder()
            .url(url)
            .post(body)
            .build()

        client.newCall(request).enqueue(object : Callback{
            override fun onFailure(call: Call,e : IOException){
                runOnUiThread{
                    Toast.makeText(this@RegistroActivity,"Error: ${e.message}",Toast.LENGTH_SHORT).show()
                }
            }

            override fun onResponse(call: Call, response: Response) {
                response.body?.string().let {
                    val jsonResponse = JSONObject(it)
                    val success = jsonResponse.getBoolean("success")
                    val message = jsonResponse.getString("message")

                    runOnUiThread {
                        Toast.makeText(this@RegistroActivity, message, Toast.LENGTH_SHORT).show()
                        if (success){
                            startActivity(Intent(this@RegistroActivity, LoginActivity::class.java))
                            finish()
                        }
                    }
                }
            }
        })
    }
}
