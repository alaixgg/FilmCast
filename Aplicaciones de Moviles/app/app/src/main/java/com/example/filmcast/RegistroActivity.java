package com.example.filmcast

import android.os.Bundle
import android.widget.Button
import android.widget.EditText
import android.widget.Toast
import androidx.appcompat.app.AppCompatActivity


class RegistroActivity : AppCompatActivity() {

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_register)

        // Referencias a los elementos del layout
        ;
        val editTextName = findViewById<EditText>(R.id.editTextName)
                val editTextEmail = findViewById<EditText>(R.id.ema)
                val editTextPassword = findViewById<EditText>(R.id.editTextPassword)
                val btnRegister = findViewById<Button>(R.id.btnRegister)
                val btnLogin = findViewById<Button>(R.id.btnLogin)

                // Acción para el botón de "Registrarse"
                btnRegister.setOnClickListener {
            val name = editTextName.text.toString()
            val email = editTextEmail.text.toString()
            val password = editTextPassword.text.toString()

            if (name.isEmpty() || email.isEmpty() || password.isEmpty()) {
                Toast.makeText(this, "Por favor, complete todos los campos", Toast.LENGTH_SHORT).show()
            } else {
                // Lógica para registrar al usuario (puedes agregar más lógica aquí)
                Toast.makeText(this, "Usuario registrado con éxito", Toast.LENGTH_SHORT).show()
            }
        }

        // Acción para el botón de "Iniciar sesión"
        btnLogin.setOnClickListener {
            // Lógica para ir a la pantalla de inicio de sesión, si es necesario
            finish() // Termina la actividad actual y vuelve a la anterior
        }
    }
}
