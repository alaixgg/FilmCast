package com.example.filmcast.ui.login

import android.content.Intent
import android.os.Bundle
import android.widget.ImageView
import androidx.activity.enableEdgeToEdge
import androidx.appcompat.app.AppCompatActivity
import com.example.filmcast.R

class ActorActivity : AppCompatActivity() {

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        enableEdgeToEdge()
        setContentView(R.layout.activity_actor)

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