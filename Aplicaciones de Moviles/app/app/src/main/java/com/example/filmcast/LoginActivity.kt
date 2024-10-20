package com.example.filmcast

import android.annotation.SuppressLint
import android.content.Intent
import android.os.Bundle
import android.text.InputType
import android.widget.Button
import android.widget.EditText
import android.widget.ImageView
import androidx.activity.enableEdgeToEdge
import androidx.appcompat.app.AppCompatActivity

class LoginActivity : AppCompatActivity() {
    @SuppressLint("MissingInflatedId")

    private var passwordVisible = false

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        enableEdgeToEdge()
        setContentView(R.layout.activity_login)

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

        }

        registerbtn.setOnClickListener{

            val intent = Intent(this, RegistroActivity::class.java)
            startActivity(intent)

        }

        }
    }