package com.example.filmcast.ui.login

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

        // Inicialización de SharedPreferences para obtener el token
        sharedPreferences = getSharedPreferences("app_preferences", MODE_PRIVATE)

        // Configurar los adaptadores para los Spinners con los valores de strings.xml
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

        // Configurar el Button para realizar la búsqueda
        btnBuscar.setOnClickListener {
            // Obtener los valores seleccionados en los Spinners y pasarlos por parseRange
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

            // Crear el objeto con los parámetros de búsqueda
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

            // Log para ver los parámetros que estamos enviando
            Log.d("ActivityBuscar", "Parámetros enviados a la API: $params")

            // Llamar a la función para realizar la búsqueda
            realizarBusqueda(params)
        }
    }

    // Configurar el Spinner
    private fun setupSpinner(spinner: Spinner, arrayResId: Int) {
        val adapter = ArrayAdapter.createFromResource(
            this,  // 'this' se refiere al contexto actual de la actividad
            arrayResId,  // El ID del array en strings.xml
            android.R.layout.simple_spinner_item  // Layout predeterminado para el spinner
        )
        adapter.setDropDownViewResource(android.R.layout.simple_spinner_dropdown_item)
        spinner.adapter = adapter
    }

    // Función para parsear rangos y convertir valores
    private fun parseRange(value: String): List<Any> {
        return try {
            // Verificar si el valor tiene un formato de rango (por ejemplo "18-22")
            val range = value.split("-")
            if (range.size == 2) {
                // Si es un rango, convertimos ambos valores a enteros y los devolvemos como lista
                listOf(range[0].toInt(), range[1].toInt())
            } else {
                // Si no es un rango, devolvemos el valor como un solo número
                listOf(value.toInt())
            }
        } catch (e: NumberFormatException) {
            // Si no es un número, devolvemos una lista con el valor como String (por ejemplo "Canada")
            listOf(value)
        }
    }

    // Función para realizar la búsqueda y enviar los parámetros a la API
    private fun realizarBusqueda(params: JSONObject) {
        // URL de la API a la que se va a hacer la solicitud
        val url = "https://model.cuspide.club/find_closest_actors"

        // Recuperar el token del SharedPreferences
        val token = getTokenFromPreferences()

        if (token == null) {
            Toast.makeText(this, "No se ha encontrado el token de sesión.", Toast.LENGTH_SHORT).show()
            return
        }

        // Crear cliente OkHttp
        val client = OkHttpClient()

        // Crear el cuerpo de la solicitud POST
        val requestBody = RequestBody.create("application/json".toMediaType(), params.toString())

        // Crear la solicitud HTTP
        val request = Request.Builder()
            .url(url)
            .post(requestBody)  // Usamos POST ya que es el método que estás utilizando en tu API
            .addHeader("Authorization", "Bearer $token")  // Agregar el token al encabezado
            .build()

        // Realizar la solicitud de forma asíncrona
        client.newCall(request).enqueue(object : Callback {
            override fun onFailure(call: Call, e: IOException) {
                // Si la solicitud falla
                runOnUiThread {
                    Toast.makeText(this@ActivityBuscar, "Error en la búsqueda: ${e.message}", Toast.LENGTH_SHORT).show()
                }
            }

            override fun onResponse(call: Call, response: Response) {
                if (response.isSuccessful) {
                    // Obtener los datos de la respuesta
                    val responseData = response.body?.string()

                    // Log para ver la respuesta completa de la API
                    Log.d("ActivityBuscar", "Respuesta de la API: $responseData")

                    // Usamos runOnUiThread para actualizar la UI en el hilo principal
                    runOnUiThread {
                        try {
                            // Si la respuesta es JSON, puedes parsearla aquí.
                            val jsonResponse = JSONObject(responseData)
                            // Ejemplo de cómo manejar la respuesta:
                            if (jsonResponse.getString("status") == "success") {
                                // Mostrar un mensaje de éxito
                                Toast.makeText(this@ActivityBuscar, "Búsqueda exitosa", Toast.LENGTH_SHORT).show()
                            } else {
                                // Manejar el caso en que la respuesta no sea exitosa
                                Toast.makeText(this@ActivityBuscar, "No se encontraron resultados", Toast.LENGTH_SHORT).show()
                            }
                        } catch (e: Exception) {
                            // En caso de error al parsear la respuesta
                            Toast.makeText(this@ActivityBuscar, "Error en la respuesta: ${e.message}", Toast.LENGTH_SHORT).show()
                        }
                    }
                } else {
                    // Si la respuesta no fue exitosa
                    runOnUiThread {
                        Toast.makeText(this@ActivityBuscar, "Error en la búsqueda", Toast.LENGTH_SHORT).show()
                    }
                }
            }
        })
    }

    private fun getTokenFromPreferences(): String? {
        return sharedPreferences.getString("token", null)
    }
}