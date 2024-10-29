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
import android.widget.Toast
import androidx.appcompat.app.AppCompatActivity
import com.google.android.gms.tasks.Task
import com.google.firebase.auth.FirebaseAuth
import com.google.firebase.firestore.FirebaseFirestore

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
                auth.createUserWithEmailAndPassword(emailText,passwordText)
                    .addOnCompleteListener(this) { task ->
                        if (task.isSuccessful){
                            val userId = auth.currentUser?.uid
                            val userMap = hashMapOf(
                                "username" to usernameText,
                                "email" to emailText
                            )
                            userId?.let {
                                firestore.collection("users").document(it)
                                    .set(userMap)
                                    .addOnCompleteListener{
                                        Toast.makeText(this, "Usuario Registrado con exito!",Toast.LENGTH_SHORT).show()
                                        val intent = Intent(this, LoginActivity::class.java)
                                        startActivity(intent)
                                        finish()
                                    }
                                    .addOnFailureListener{e ->
                                        Toast. makeText(this, "Error al guardar datos: ${e.message}", Toast.LENGTH_SHORT).show()
                                    }
                            }
                        }
                        else {
                            Toast.makeText(this, "Error: ${task.exception?.message}", Toast.LENGTH_SHORT).show()
                        }
                    }
            }
            else {
                Toast.makeText(this, "por favor ingresa todos los campos", Toast.LENGTH_SHORT).show()
            }

        }

    }
}
