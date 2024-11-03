package com.example.filmcast.ui.login

import android.content.Intent
import android.os.Bundle
import android.widget.Button
import android.widget.ImageView
import androidx.activity.enableEdgeToEdge
import androidx.appcompat.app.AppCompatActivity
import com.example.filmcast.R

class GuardadosActivity : AppCompatActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        enableEdgeToEdge()
        setContentView(R.layout.activity_actores_lista)
        val volver= findViewById<Button>(R.id.GA_boton_volver)
        volver.setOnClickListener{
            val intent = Intent(this, menuActivity::class.java)
            startActivity(intent)
        }
        val buscar= findViewById<Button>(R.id.menu_button_buscar)
        volver.setOnClickListener{
            val intent = Intent(this, ActivityBuscar::class.java)
            startActivity(intent)
        }
        val perfil = findViewById<ImageView>(R.id.PA_perfil)
        perfil.setOnClickListener {
            val intent = Intent(this, PerfilActivity::class.java)
            startActivity(intent)
        }
        val menu = findViewById<ImageView>(R.id.Pa_menu)
        menu.setOnClickListener {
            val intent = Intent(this, menuActivity::class.java)
            startActivity(intent)
        }





    }


    }
