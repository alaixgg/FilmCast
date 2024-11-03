package com.example.filmcast.ui.login

import android.os.Bundle
import android.widget.Button
import androidx.activity.enableEdgeToEdge
import androidx.activity.result.contract.ActivityResultContracts
import androidx.appcompat.app.AppCompatActivity
import android.content.Intent
import android.widget.Toast
import com.example.filmcast.R
import com.example.filmcast.data.RetroFit.RegistroRequest
import com.example.filmcast.data.RetroFit.RetrofitInstance
import kotlinx.coroutines.CoroutineScope
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.launch
import kotlinx.coroutines.withContext

class RegistroActivity<EditText> : AppCompatActivity() {

    private lateinit var et_Username: EditText
    private lateinit var et_Password: EditText
    private lateinit var et_confirpassword: EditText
    private lateinit var btn_register: Button

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_register) // Asegúrate de que el layout esté configurado

        et_Username = findViewById(R.id.et_username)
        et_Password = findViewById(R.id.et_password)
        et_confirpassword = findViewById(R.id.et_confirpassword)
        btn_register = findViewById(R.id.btn_register)

        btn_register.setOnClickListener {
            val usuario = et_Username.text.toString().trim()
            val contrasena = et_Password.text.toString()
            val confirmarContrasena = et_confirpassword.text.toString()

            if (contrasena != confirmarContrasena) {
                Toast.makeText(this, "Las contraseñas no coinciden", Toast.LENGTH_SHORT).show()
            } else {
                registrarUsuario(usuario, contrasena)
            }
        }
    }

    private fun registrarUsuario(usuario: String, contrasena: String) {
        val request = RegistroRequest(
            nombre = usuario,
            clave = contrasena
        )

        CoroutineScope(Dispatchers.IO).launch {
            try {
                val response = RetrofitInstance.api.registrarUsuario(request)
                if (response.isSuccessful) {
                    withContext(Dispatchers.Main) {
                        Toast.makeText(this@RegistroActivity, "Registro exitoso", Toast.LENGTH_SHORT).show()
                        // Redirige a la actividad de login o realiza otras acciones
                        finish()
                    }
                } else {
                    withContext(Dispatchers.Main) {
                        Toast.makeText(this@RegistroActivity, "Error en el registro: ${response.message()}", Toast.LENGTH_SHORT).show()
                    }
                }
            } catch (e: Exception) {
                withContext(Dispatchers.Main) {
                    Toast.makeText(this@RegistroActivity, "Ocurrió un error: ${e.message}", Toast.LENGTH_SHORT).show()
                }
            }
        }
    }
}

