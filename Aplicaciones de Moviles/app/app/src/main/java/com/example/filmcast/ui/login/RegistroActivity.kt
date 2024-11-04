package com.example.filmcast.ui.login

import android.annotation.SuppressLint
import android.os.Bundle
import android.widget.Button
import androidx.activity.enableEdgeToEdge
import androidx.appcompat.app.AppCompatActivity
import android.content.Intent
import android.text.InputType
import android.widget.EditText
import android.widget.ImageView
import android.widget.Toast
import com.example.filmcast.R
import okhttp3.Call
import okhttp3.Callback
import okhttp3.MediaType.Companion.toMediaType
import okhttp3.OkHttpClient
import okhttp3.Request
import okhttp3.RequestBody.Companion.toRequestBody
import okhttp3.Response
import org.json.JSONObject
import java.io.IOException

class RegistroActivity : AppCompatActivity() {

    private var passwordVisible = false

    @SuppressLint("MissingInflatedId")
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_register)

        val username = findViewById<EditText>(R.id.et_username)
        val password = findViewById<EditText>(R.id.et_password)
        val password1 = findViewById<EditText>(R.id.et_password1)
        val loginbtn = findViewById<Button>(R.id.btn_login)
        val registerbtn = findViewById<Button>(R.id.btn_register)
        val togglebtn = findViewById<ImageView>(R.id.passwordVisibilityToggle)

        //boton para mostrar/esconder contraseña
        togglebtn.setOnClickListener{
            if (passwordVisible) {
                password1.inputType =
                    InputType.TYPE_CLASS_TEXT or InputType.TYPE_TEXT_VARIATION_PASSWORD
            } else {
                password1.inputType = InputType.TYPE_CLASS_TEXT or InputType.TYPE_TEXT_VARIATION_VISIBLE_PASSWORD
            }

            password1.setSelection(password1.text.length)
            passwordVisible = !passwordVisible
        }

        //boton para ir al LoginActivity
        loginbtn.setOnClickListener{
            val intent = Intent(this,LoginActivity::class.java)
            startActivity(intent)
        }

        registerbtn.setOnClickListener{
            val usernameText = username.text.toString().trim()
            val passwordText = password.text.toString().trim()
            val password1Text = password1.text.toString().trim()

            if (passwordText != password1Text){
                Toast.makeText(this,"Las contraseñas no coinciden.", Toast.LENGTH_SHORT).show()
            }
            else {
                if (usernameText.isNotEmpty() && passwordText.isNotEmpty() && password1Text.isNotEmpty()){
                    registrarUsuario(usernameText,passwordText,password1Text)
                }
                else {
                    Toast.makeText(this,"Por favor ingresa todos los campos.", Toast.LENGTH_SHORT).show()
                }
            }

        }


    }

    private fun registrarUsuario(usernameText: String, emailText: String, passwordText: String) {
        val url = "https://db.cuspide.club/registro"

        //crear json con los datos de usuario
        val json =  JSONObject()
        json.put("nombre",usernameText)
        json.put("clave",passwordText)

        //solicitud HTTP POST
        val mediaType = "application/json; charset=utf-8".toMediaType()
        val body = json.toString().toRequestBody(mediaType)

        val client = OkHttpClient()
        val request = Request.Builder()
            .url(url)
            .post(body)
            .build()

        client.newCall(request).enqueue(object : Callback {
            override fun onFailure(call: Call, e : IOException){
                runOnUiThread{
                    Toast.makeText(this@RegistroActivity,"Error: ${e.message}", Toast.LENGTH_SHORT).show()
                }
            }

            override fun onResponse(call: Call, response: Response) {
                if (response.isSuccessful){
                    runOnUiThread{
                        Toast.makeText(this@RegistroActivity,"Registro exitoso.", Toast.LENGTH_SHORT).show()
                        startActivity(Intent(this@RegistroActivity,LoginActivity::class.java))
                        finish()
                    }
                }
                else{
                    runOnUiThread{
                        Toast.makeText(this@RegistroActivity,"Error al registrar el usuario.", Toast.LENGTH_SHORT).show()
                    }
                }
            }
        })
    }

}

