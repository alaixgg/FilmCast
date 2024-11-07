package com.example.filmcast.ui.login

import android.content.Intent
import android.content.SharedPreferences
import android.os.Bundle
import android.util.Log
import android.widget.ArrayAdapter
import android.widget.Button
import android.widget.Spinner
import android.widget.Toast
import androidx.appcompat.app.AppCompatActivity
import com.example.filmcast.R
import okhttp3.*
import okhttp3.MediaType.Companion.toMediaType
import org.json.JSONObject
import java.io.IOException
import java.util.ArrayList

class ActivityBuscar : AppCompatActivity() {

    private lateinit var spinnerEdad: Spinner
    private lateinit var spinnerGeneroCine: Spinner
    private lateinit var spinnerEducacion: Spinner
    private lateinit var spinnerSalario: Spinner
    private lateinit var spinnerAniosAct: Spinner
    private lateinit var spinnerGenero: Spinner
    private lateinit var spinnerHabilidad: Spinner
    private lateinit var spinnerLikes: Spinner
    private lateinit var spinnerBelleza: Spinner
    private lateinit var spinnerSeguidores: Spinner
    private lateinit var spinnerPremios: Spinner
    private lateinit var spinnerMenciones: Spinner
    private lateinit var spinnerTamañoPagina: Spinner
    private lateinit var btnBuscar: Button
    private lateinit var sharedPreferences: SharedPreferences

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_buscar)

        spinnerEdad = findViewById(R.id.BU_spinner_edad)
        spinnerGeneroCine = findViewById(R.id.BU_genero_cine)
        spinnerEducacion = findViewById(R.id.BU_spinner_educacion)
        spinnerSalario = findViewById(R.id.BU_spinner_salario)
        spinnerAniosAct = findViewById(R.id.BU_spinner_años_act)
        spinnerGenero = findViewById(R.id.BU_spinner_genero)
        spinnerHabilidad = findViewById(R.id.BU_spinner_habilidad)
        spinnerLikes = findViewById(R.id.BU_spinner_redes_likes)
        spinnerBelleza = findViewById(R.id.BU_spinner_belleza)
        spinnerSeguidores = findViewById(R.id.BU_spinner_redes_seguidores)
        spinnerPremios = findViewById(R.id.Bu_spinner_premios)
        spinnerMenciones = findViewById(R.id.BU_spinner_menciones)
        spinnerTamañoPagina = findViewById(R.id.BU_spinner_Tamaño_pagina)
        btnBuscar = findViewById(R.id.Bu_Boton_Buscar)


        sharedPreferences = getSharedPreferences("app_preferences", MODE_PRIVATE)

        setupSpinner(spinnerEdad, R.array.Bu_edad)
        setupSpinner(spinnerGeneroCine, R.array.Bu_Cinematigrafia)
        setupSpinner(spinnerEducacion, R.array.Bu_educacion)
        setupSpinner(spinnerSalario, R.array.Bu_salario)
        setupSpinner(spinnerAniosAct, R.array.Bu_Belleza)
        setupSpinner(spinnerGenero, R.array.Bu_genero)
        setupSpinner(spinnerLikes, R.array.Bu_likes)
        setupSpinner(spinnerBelleza, R.array.Bu_Belleza)
        setupSpinner(spinnerSeguidores, R.array.Bu_seguidores)
        setupSpinner(spinnerHabilidad, R.array.Bu_habilidad)
        setupSpinner(spinnerPremios, R.array.Bu_premios)
        setupSpinner(spinnerMenciones, R.array.Bu_Menciones)
        setupSpinner(spinnerTamañoPagina, R.array.Bu_tamaño_pag)


        btnBuscar.setOnClickListener {

            val edad = parseRange(spinnerEdad.selectedItem.toString())
            val aniosAct = parseRange(spinnerAniosAct.selectedItem.toString())
            val belleza = parseRange(spinnerBelleza.selectedItem.toString())
            val habilidad = parseRange(spinnerHabilidad.selectedItem.toString())
            val premios = parseRange(spinnerPremios.selectedItem.toString())
            val menciones = parseRange(spinnerMenciones.selectedItem.toString())
            val seguidores = parseRange(spinnerSeguidores.selectedItem.toString())
            val likes = parseRange(spinnerLikes.selectedItem.toString())
            val tamañoPagina = parseRange(spinnerTamañoPagina.selectedItem.toString())
            val salario = parseRange(spinnerSalario.selectedItem.toString())


            val params = JSONObject().apply {
                put("predecir", JSONObject().apply {
                    put("Age", edad)
                    put("Years Active", aniosAct)
                    put("Beauty", belleza)
                    put("Skill Level", habilidad)
                    put("Award Wins", premios)
                    put("Media Mentions", menciones)
                    put("Social Media Followers", seguidores)
                    put("Social Media Likes", likes)
                    put("Network Size", tamañoPagina)
                    put("Income", salario)
                })
            }


            Log.d("ActivityBuscar", "Parámetros enviados a la API: $params")


            realizarBusqueda(params)
        }
    }


    private fun setupSpinner(spinner: Spinner, arrayResId: Int) {
        val adapter = ArrayAdapter.createFromResource(
            this,
            arrayResId,
            android.R.layout.simple_spinner_item
        )
        adapter.setDropDownViewResource(android.R.layout.simple_spinner_dropdown_item)
        spinner.adapter = adapter
    }


    private fun parseRange(value: String): List<Any> {
        return try {

            val range = value.split("-")
            if (range.size == 2) {

                listOf(range[0].toInt(), range[1].toInt())
            } else {

                listOf(value.toInt())
            }
        } catch (e: NumberFormatException) {

            listOf(value)
        }
    }


    private fun realizarBusqueda(params: JSONObject) {

        val url = "https://model.cuspide.club/find_closest_actors"


        val token = getTokenFromPreferences()

        if (token == null) {
            Toast.makeText(this, "No se ha encontrado el token de sesión.", Toast.LENGTH_SHORT).show()
            return
        }


        val client = OkHttpClient()


        // val requestBody = RequestBody.create("application/json".toMediaType(), params.toString())
        val requestBody = RequestBody.create("application/json".toMediaType(), params.toString())


        val request = Request.Builder()
            .url(url)
            .post(requestBody)  // Usamos POST ya que es el método que estás utilizando en tu API
            .addHeader("Authorization", "Bearer $token")  // Agregar el token al encabezado
            .build()


        client.newCall(request).enqueue(object : Callback {
            override fun onFailure(call: Call, e: IOException) {

                runOnUiThread {
                    Toast.makeText(this@ActivityBuscar, "Error en la búsqueda: ${e.message}", Toast.LENGTH_SHORT).show()
                }
            }

            private val actorIds = mutableListOf<String>()

            override fun onResponse(call: Call, response: Response) {
                if (response.isSuccessful) {

                    val responseData = response.body?.string()


                    Log.d("ActivityBuscar", "Respuesta de la API: $responseData")


                    runOnUiThread {
                        try {
                            val jsonResponse = JSONObject(responseData)

                            if (jsonResponse.getString("status") == "success") {
                                val actorId = jsonResponse.getJSONArray("actor_id")

                                actorIds.clear()

                                for (i in 0 until actorId.length()) {
                                    actorIds.add(actorId.getString(i))
                                }

                                Toast.makeText(this@ActivityBuscar, "Búsqueda exitosa", Toast.LENGTH_SHORT).show()
                            } else {
                                Toast.makeText(this@ActivityBuscar, "No se encontraron resultados", Toast.LENGTH_SHORT).show()
                            }
                        } catch (e: Exception) {

                            Toast.makeText(this@ActivityBuscar, "Error en la respuesta: ${e.message}", Toast.LENGTH_SHORT).show()
                        }
                    }
                } else {

                    runOnUiThread {
                        Toast.makeText(this@ActivityBuscar, "Error en la búsqueda", Toast.LENGTH_SHORT).show()
                    }
                }
                val intent = Intent(this@ActivityBuscar, ResultadoActivity::class.java)
                intent.putStringArrayListExtra("ACTOR_IDS", ArrayList(actorIds))
                startActivity(intent)
            }
        })
    }

    private fun getTokenFromPreferences(): String? {
        return sharedPreferences.getString("token", null)
    }
}