package com.example.filmcast.ui.login

import android.content.Intent
import android.os.Bundle
import android.widget.ImageView
import android.widget.Toast
import androidx.appcompat.app.AppCompatActivity
import com.example.filmcast.R
import com.example.filmcast.data.RetroFit.ApiService
import com.example.filmcast.data.RetroFit.Proyecto
import com.example.filmcast.databinding.ActivityCreaProyectoBinding
import retrofit2.Retrofit
import retrofit2.converter.gson.GsonConverterFactory

class Crea_proyecto : AppCompatActivity() {

    private lateinit var binding: ActivityCreaProyectoBinding

    // Inicializa Retrofit y ApiService
    private val retrofit by lazy {
        Retrofit.Builder()
            .baseUrl("https://api.example.com/")
            .addConverterFactory(GsonConverterFactory.create())
            .build()
    }

    private val apiService by lazy {
        retrofit.create(ApiService::class.java)
    }

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        binding = ActivityCreaProyectoBinding.inflate(layoutInflater)
        setContentView(binding.root)

        // Configuración de listeners para los botones
        binding.ProGuardarProyecto.setOnClickListener {
            guardarProyecto()
        }

        val perfil = findViewById<ImageView>(R.id.BU_perfil)
        perfil.setOnClickListener {
            val intent = Intent(this, PerfilActivity::class.java)
            startActivity(intent)
        }

        val menu = findViewById<ImageView>(R.id.Bu_menu)
        menu.setOnClickListener {
            val intent = Intent(this, menuActivity::class.java)
            startActivity(intent)
        }
    }

    private fun guardarProyecto() {
        val nombreProyecto = binding.ProNombreProyecto.text.toString()
        val descripcionProyecto = binding.ProDescripcionProyecto.text.toString()
        val generoCinematografico = binding.ProGeneroCinematografico.text.toString()
        val fechaInicio = binding.ProFechaInicio.text.toString()
        val fechaFin = binding.ProFechaFin.text.toString()
        val presupuesto = binding.ProPresupuesto.text.toString().toDoubleOrNull()

        if (nombreProyecto.isNotEmpty() && descripcionProyecto.isNotEmpty() &&
            generoCinematografico.isNotEmpty() && fechaInicio.isNotEmpty() &&
            fechaFin.isNotEmpty() && presupuesto != null) {

            val proyecto = Proyecto(
                nombre = nombreProyecto,
                descripcion = descripcionProyecto,
                genero = generoCinematografico,
                fechaInicio = fechaInicio,
                fechaFin = fechaFin,
                presupuesto = presupuesto
            )


        } else {
            Toast.makeText(this, "Por favor, completa todos los campos", Toast.LENGTH_SHORT).show()
        }
    }
}