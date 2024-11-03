package com.example.filmcast.ui.login

import android.content.Intent
import android.os.Bundle
import android.widget.ArrayAdapter
import android.widget.Button
import android.widget.ImageView
import android.widget.Spinner
import android.widget.Toast
import androidx.appcompat.app.AppCompatActivity
import com.example.filmcast.R
import com.example.filmcast.data.RetroFit.RetrofitClient
import com.example.filmcast.data.RetroFit.SeleccionData
import retrofit2.Call
import retrofit2.Callback
import retrofit2.Response

class ActivityBuscar : AppCompatActivity() {

    private lateinit var spinnerEdad: Spinner
    private lateinit var spinnerSalario: Spinner
    private lateinit var spinnerAniosAct: Spinner
    private lateinit var spinnerLikes: Spinner
    private lateinit var spinnerBeLleza: Spinner
    private lateinit var spinnerSeguidores: Spinner
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
        spinnerSalario = findViewById(R.id.BU_spinner_salario)
        spinnerAniosAct = findViewById(R.id.BU_spinner_años_act)
        spinnerLikes = findViewById(R.id.BU_spinner_redes_likes)
        spinnerBeLleza = findViewById(R.id.BU_spinner_belleza)
        spinnerSeguidores = findViewById(R.id.BU_spinner_redes_seguidores)
        spinnerPremios = findViewById(R.id.Bu_spinner_premios)
        spinnerMenciones = findViewById(R.id.BU_spinner_menciones)
        spinnerTamañoPagina = findViewById(R.id.BU_spinner_Tamaño_pagina)

        val edades = arrayOf("Selecciona edad", "Menos de 20", "20-30", "31-40", "41-50", "Más de 50")
        val salarios = arrayOf("Selecciona salario", "Menos de 1000", "1000-2000", "2001-3000", "Más de 3000")
        val añosAct = arrayOf("Selecciona años de actividad", "Menos de 1", "1-5", "6-10", "Más de 10")
        val likes = arrayOf("Selecciona # Likes", "0–500", "501–1500", "1501–3000", "3001–4500", "4501–6000", "6001 o más")
        val belleza = arrayOf("Selecciona Nivel Belleza", "0-2", "3-5", "6-8", "9-10")
        val seguidores = arrayOf("Selecciona # seguidores", "0–1000", "1001–8000", "8001–12.000", "12.001–18.000", "18.001–24.001", "24.001 o más")
        val premios = arrayOf("Selecciona premios", "Ninguno", "1-3", "4-6", "Más de 6")
        val menciones = arrayOf("Selecciona menciones", "Ninguna", "1-5", "6-10", "Más de 10")
        val tamañosPagina = arrayOf("Selecciona tamaño de página", "10", "20", "50", "100")

        val adapterEdad = ArrayAdapter(this, android.R.layout.simple_spinner_item, edades)
        val adapterSalario = ArrayAdapter(this, android.R.layout.simple_spinner_item, salarios)
        val adapterAniosAct = ArrayAdapter(this, android.R.layout.simple_spinner_item, añosAct)
        val adapterLikes = ArrayAdapter(this, android.R.layout.simple_spinner_item, likes)
        val adapterBeLleza = ArrayAdapter(this, android.R.layout.simple_spinner_item, belleza)
        val adapterSeguidores = ArrayAdapter(this, android.R.layout.simple_spinner_item, seguidores)
        val adapterPremios = ArrayAdapter(this, android.R.layout.simple_spinner_item, premios)
        val adapterMenciones = ArrayAdapter(this, android.R.layout.simple_spinner_item, menciones)
        val adapterTamañoPagina = ArrayAdapter(this, android.R.layout.simple_spinner_item, tamañosPagina)

        adapterEdad.setDropDownViewResource(android.R.layout.simple_spinner_dropdown_item)
        adapterSalario.setDropDownViewResource(android.R.layout.simple_spinner_dropdown_item)
        adapterAniosAct.setDropDownViewResource(android.R.layout.simple_spinner_dropdown_item)
        adapterLikes.setDropDownViewResource(android.R.layout.simple_spinner_dropdown_item)
        adapterBeLleza.setDropDownViewResource(android.R.layout.simple_spinner_dropdown_item)
        adapterSeguidores.setDropDownViewResource(android.R.layout.simple_spinner_dropdown_item)
        adapterPremios.setDropDownViewResource(android.R.layout.simple_spinner_dropdown_item)
        adapterMenciones.setDropDownViewResource(android.R.layout.simple_spinner_dropdown_item)
        adapterTamañoPagina.setDropDownViewResource(android.R.layout.simple_spinner_dropdown_item)

        spinnerEdad.adapter = adapterEdad
        spinnerSalario.adapter = adapterSalario
        spinnerAniosAct.adapter = adapterAniosAct
        spinnerLikes.adapter = adapterLikes
        spinnerBeLleza.adapter = adapterBeLleza
        spinnerSeguidores.adapter = adapterSeguidores
        spinnerPremios.adapter = adapterPremios
        spinnerMenciones.adapter = adapterMenciones
        spinnerTamañoPagina.adapter = adapterTamañoPagina

        val enviarButton = findViewById<Button>(R.id.Bu_Boton_Buscar)

        enviarButton.setOnClickListener {
            val seleccionData = SeleccionData(
                edad = spinnerEdad.selectedItem.toString(),
                salario = spinnerSalario.selectedItem.toString(),
                aniosAct = spinnerAniosAct.selectedItem.toString(),
                likes = spinnerLikes.selectedItem.toString(),
                belleza = spinnerBeLleza.selectedItem.toString(),
                seguidores = spinnerSeguidores.selectedItem.toString(),
                premios = spinnerPremios.selectedItem.toString(),
                menciones = spinnerMenciones.selectedItem.toString(),
                tamañoPagina = spinnerTamañoPagina.selectedItem.toString()
            )


            enviarSeleccion(seleccionData)
        }
    }

    private fun enviarSeleccion(data: SeleccionData) {
        RetrofitClient.instance.enviarSeleccion(data).enqueue(object : Callback<Void> {
            override fun onResponse(call: Call<Void>, response: Response<Void>) {
                if (response.isSuccessful) {
                    Toast.makeText(this@ActivityBuscar, "Selección enviada", Toast.LENGTH_SHORT).show()
                } else {
                    Toast.makeText(this@ActivityBuscar, "Error al enviar", Toast.LENGTH_SHORT).show()
                }
            }

            override fun onFailure(call: Call<Void>, t: Throwable) {
                Toast.makeText(this@ActivityBuscar, "Error de conexión: ${t.message}", Toast.LENGTH_SHORT).show()
            }
        })
    }
}
