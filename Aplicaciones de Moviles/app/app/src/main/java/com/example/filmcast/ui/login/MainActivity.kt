package com.example.filmcast.ui.login

import android.os.Bundle
import android.widget.Button
import androidx.activity.enableEdgeToEdge
import androidx.appcompat.app.AppCompatActivity
import android.content.Intent
import com.example.filmcast.R

class MainActivity : AppCompatActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        enableEdgeToEdge()
        setContentView(R.layout.activity_login)
        val IS_registro= findViewById<Button>(R.id.IS_Register)
        IS_registro.setOnClickListener{
            val intent = Intent(this, RegistroActivity::class.java)
            startActivity(intent)
        }

        val IS_Iniciar_sesion= findViewById<Button>(R.id.IS_iniciar_sesion)
        IS_Iniciar_sesion.setOnClickListener{
            val intent = Intent(this, menuActivity::class.java)
            startActivity(intent)

            //--ydfggtytsfydg-->
        }
    }
}