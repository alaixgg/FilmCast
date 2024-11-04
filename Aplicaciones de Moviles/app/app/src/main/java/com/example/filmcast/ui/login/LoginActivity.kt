package com.example.filmcast.ui.login

import android.os.Bundle
import android.widget.Button
import androidx.activity.enableEdgeToEdge
import androidx.appcompat.app.AppCompatActivity
import android.content.Intent
import android.text.InputType
import android.widget.EditText
import android.widget.ImageView
import android.widget.Toast
import android.content.Context
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

class LoginActivity : AppCompatActivity() {

    private var passwordVisible = false

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)

        // Verifica si ya hay una sesión iniciada
        val sharedPreferences = getSharedPreferences("Sesion", Context.MODE_PRIVATE)
        val sesionIniciada = sharedPreferences.getBoolean("sesion_iniciada", false)

        if (sesionIniciada) {
            // Redirige directamente a MenuActivity si la sesión está iniciada
            val intent = Intent(this, MenuActivity::class.java)
            startActivity(intent)
            finish()
            return
        }

        enableEdgeToEdge()
        setContentView(R.layout.activity_login)

        val username = findViewById<EditText>(R.id.et_username)
        val password = findViewById<EditText>(R.id.et_password)
        val IS_registro = findViewById<Button>(R.id.btn_register)
        val IS_Iniciar_sesion = findViewById<Button>(R.id.btn_login)
        val togglebtn = findViewById<ImageView>(R.id.passwordVisibilityToggle)

        //boton para mostrar/ocultar contraseña
        togglebtn.setOnClickListener {
            if (passwordVisible) {
                password.inputType =
                    InputType.TYPE_CLASS_TEXT or InputType.TYPE_TEXT_VARIATION_PASSWORD
            } else {
                password.inputType =
                    InputType.TYPE_CLASS_TEXT or InputType.TYPE_TEXT_VARIATION_VISIBLE_PASSWORD
            }
            password.setSelection(password.text.length)
            passwordVisible = !passwordVisible
        }

        IS_registro.setOnClickListener {
            val intent = Intent(this, RegistroActivity::class.java)
            startActivity(intent)
        }

        IS_Iniciar_sesion.setOnClickListener {
            val usernameText = username.text.toString().trim()
            val passwordText = password.text.toString().trim()

            if (usernameText.isNotEmpty() && passwordText.isNotEmpty()) {
                iniciarSesion(usernameText, passwordText)
            } else {
                Toast.makeText(this, "Por favor, ingresa todos los campos.", Toast.LENGTH_SHORT)
                    .show()
            }
        }
    }

    private fun iniciarSesion(emailText: String, passwordText: String) {
        val url = "https://db.cuspide.club/login" // Reemplaza con tu URL de login en el servidor

        val json = JSONObject()
        json.put("nombre", emailText)
        json.put("clave", passwordText)

        val mediaType = "application/json; charset=utf-8".toMediaType()
        val body = json.toString().toRequestBody(mediaType)

        val client = OkHttpClient()
        val request = Request.Builder()
            .url(url)
            .post(body)
            .build()

        client.newCall(request).enqueue(object : Callback {
            override fun onFailure(call: Call, e: IOException) {
                runOnUiThread {
                    Toast.makeText(
                        this@LoginActivity,
                        "Error de conexión: ${e.message}",
                        Toast.LENGTH_SHORT
                    ).show()
                }
            }

            override fun onResponse(call: Call, response: Response) {
                runOnUiThread {
                    when (response.code) {
                        200 -> {
                            val responseBody = response.body?.string()
                            val jsonResponse = JSONObject(responseBody ?: "")
                            val token = jsonResponse.getString("token")

                            guardarToken(token)
                            guardarSesion()

                            Toast.makeText(this@LoginActivity, "Inicio de sesión exitoso.", Toast.LENGTH_SHORT).show()
                            val intent = Intent(this@LoginActivity, MenuActivity::class.java)
                            startActivity(intent)
                            finish()//holi
                        }

                        400, 401 -> {
                            val responseBody = response.body?.string()
                            val jsonResponse = JSONObject(responseBody ?: "")
                            val errorMessage =
                                jsonResponse.optString("error", "Error en las credenciales")
                            Toast.makeText(this@LoginActivity, errorMessage, Toast.LENGTH_SHORT)
                                .show()
                        }

                        else -> {
                            Toast.makeText(
                                this@LoginActivity,
                                "Error en el servidor. Intente mas tarde.",
                                Toast.LENGTH_SHORT
                            ).show()
                        }
                    }
                }
            }
        })
    }

    private fun guardarToken(token: String) {
        val sharedPreferences = getSharedPreferences("AppPrefs", Context.MODE_PRIVATE)
        val editor = sharedPreferences.edit()
        editor.putString("token", token)
        editor.apply()
    }

    private fun guardarSesion() {
        val sharedPreferences = getSharedPreferences("Sesion", Context.MODE_PRIVATE)
        val editor = sharedPreferences.edit()
        editor.putBoolean("sesion_iniciada", true)
        editor.apply()
    }

}