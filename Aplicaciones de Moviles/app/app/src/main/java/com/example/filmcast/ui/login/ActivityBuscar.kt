package com.example.filmcast.ui.login

import android.content.Intent
import com.example.filmcast.R
import android.os.Bundle
import android.widget.ArrayAdapter
import android.widget.ImageView
import android.widget.Spinner
import androidx.appcompat.app.AppCompatActivity

class ActivityBuscar : AppCompatActivity() {

    private lateinit var spinnerEdad: Spinner
    private lateinit var spinnerGeneroCine: Spinner
    private lateinit var spinnerEducacion: Spinner
    private lateinit var spinnerSalario: Spinner
    private lateinit var spinnerAniosAct: Spinner
    private lateinit var spinnerGenero: Spinner
    private lateinit var spinnerNacionalidad: Spinner
    private lateinit var spinnerPremios: Spinner
    private lateinit var spinnerMenciones: Spinner
    private lateinit var spinnerTamañoPagina: Spinner

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_buscar)

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


        spinnerEdad = findViewById(R.id.BU_spinner_edad)
        spinnerGeneroCine = findViewById(R.id.BU_genero_cine)
        spinnerEducacion = findViewById(R.id.BU_spinner_educacion)
        spinnerSalario = findViewById(R.id.BU_spinner_salario)
        spinnerAniosAct = findViewById(R.id.BU_spinner_años_act)
        spinnerGenero = findViewById(R.id.BU_spinner_genero)
        spinnerNacionalidad = findViewById(R.id.BU_spinner_nacionalidad)
        spinnerPremios = findViewById(R.id.Bu_spinner_premios)
        spinnerMenciones = findViewById(R.id.BU_spinner_menciones)
        spinnerTamañoPagina = findViewById(R.id.BU_spinner_Tamaño_pagina)

        val edades = arrayOf("Selecciona edad", "Menos de 20", "20-30", "31-40", "41-50", "Más de 50")
        val generosCine = arrayOf("Selecciona género", "Acción", "Drama", "Comedia", "Terror", "Ciencia ficción")
        val educaciones = arrayOf("Selecciona nivel educativo", "Primaria", "Secundaria", "Universidad")
        val salarios = arrayOf("Selecciona salario", "Menos de 1000", "1000-2000", "2001-3000", "Más de 3000")
        val añosAct = arrayOf("Selecciona años de actividad", "Menos de 1", "1-5", "6-10", "Más de 10")
        val generos = arrayOf("Selecciona género", "Masculino", "Femenino", "Otro")
        val nacionalidades = arrayOf("Selecciona nacionalidad", "Colombiana", "Mexicana", "Argentina", "Otro")
        val premios = arrayOf("Selecciona premios", "Ninguno", "1-3", "4-6", "Más de 6")
        val menciones = arrayOf("Selecciona menciones", "Ninguna", "1-5", "6-10", "Más de 10")
        val tamañosPagina = arrayOf("Selecciona tamaño de página", "10", "20", "50", "100")


        val adapterEdad = ArrayAdapter(this, android.R.layout.simple_spinner_item, edades)
        val adapterGeneroCine = ArrayAdapter(this, android.R.layout.simple_spinner_item, generosCine)
        val adapterEducacion = ArrayAdapter(this, android.R.layout.simple_spinner_item, educaciones)
        val adapterSalario = ArrayAdapter(this, android.R.layout.simple_spinner_item, salarios)
        val adapterAniosAct = ArrayAdapter(this, android.R.layout.simple_spinner_item, añosAct)
        val adapterGenero = ArrayAdapter(this, android.R.layout.simple_spinner_item, generos)
        val adapterNacionalidad = ArrayAdapter(this, android.R.layout.simple_spinner_item, nacionalidades)
        val adapterPremios = ArrayAdapter(this, android.R.layout.simple_spinner_item, premios)
        val adapterMenciones = ArrayAdapter(this, android.R.layout.simple_spinner_item, menciones)
        val adapterTamañoPagina = ArrayAdapter(this, android.R.layout.simple_spinner_item, tamañosPagina)


        adapterEdad.setDropDownViewResource(android.R.layout.simple_spinner_dropdown_item)
        adapterGeneroCine.setDropDownViewResource(android.R.layout.simple_spinner_dropdown_item)
        adapterEducacion.setDropDownViewResource(android.R.layout.simple_spinner_dropdown_item)
        adapterSalario.setDropDownViewResource(android.R.layout.simple_spinner_dropdown_item)
        adapterAniosAct.setDropDownViewResource(android.R.layout.simple_spinner_dropdown_item)
        adapterGenero.setDropDownViewResource(android.R.layout.simple_spinner_dropdown_item)
        adapterNacionalidad.setDropDownViewResource(android.R.layout.simple_spinner_dropdown_item)
        adapterPremios.setDropDownViewResource(android.R.layout.simple_spinner_dropdown_item)
        adapterMenciones.setDropDownViewResource(android.R.layout.simple_spinner_dropdown_item)
        adapterTamañoPagina.setDropDownViewResource(android.R.layout.simple_spinner_dropdown_item)

        spinnerEdad.adapter = adapterEdad
        spinnerGeneroCine.adapter = adapterGeneroCine
        spinnerEducacion.adapter = adapterEducacion
        spinnerSalario.adapter = adapterSalario
        spinnerAniosAct.adapter = adapterAniosAct
        spinnerGenero.adapter = adapterGenero
        spinnerNacionalidad.adapter = adapterNacionalidad
        spinnerPremios.adapter = adapterPremios
        spinnerMenciones.adapter = adapterMenciones
        spinnerTamañoPagina.adapter = adapterTamañoPagina
    }
}