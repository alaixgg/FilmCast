package com.example.filmcast.ui.login

import android.os.Bundle
import android.widget.Button

import androidx.appcompat.app.AppCompatActivity
import com.example.filmcast.R

class EditarPerfil : AppCompatActivity() {

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_editar_perfil)

        val volverButton = findViewById<Button>(R.id.EDP_Cancelar)
        volverButton.setOnClickListener {
            onBackPressed()
        }


    }

}
