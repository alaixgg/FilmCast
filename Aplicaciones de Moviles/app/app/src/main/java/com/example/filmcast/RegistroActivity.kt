package com.example.filmcast

import android.annotation.SuppressLint
import android.content.Intent
import android.media.Image
import android.os.Bundle
import android.renderscript.ScriptGroup.Input
import android.text.InputType
import android.widget.Button
import android.widget.EditText
import android.widget.ImageView
import androidx.appcompat.app.AppCompatActivity

class RegistroActivity : AppCompatActivity() {
    @SuppressLint("MissingInflatedId", "CutPasteId")

    private var passwordVisible = false

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_register)

        val username = findViewById<EditText>(R.id.et_username)
        val email = findViewById<EditText>(R.id.et_email)
        val password = findViewById<EditText>(R.id.et_password)
        val loginbtn = findViewById<Button>(R.id.btn_login)
        val registerbtn = findViewById<Button>(R.id.btn_register)
        val togglebtn = findViewById<ImageView>(R.id.passwordVisibilityToggle)

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

        loginbtn.setOnClickListener{
            val intent = Intent(this,LoginActivity::class.java)
            startActivity(intent)
        }

    }
}
