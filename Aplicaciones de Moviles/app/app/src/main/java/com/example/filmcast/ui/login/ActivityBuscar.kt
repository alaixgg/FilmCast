package com.example.filmcast.ui.login

import android.content.Context
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

        Log.d("ActivityBuscar", "onCreate: Actividad iniciada.")

        // Inicializar los spinners
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

        // Obtener las SharedPreferences
        sharedPreferences = getSharedPreferences("app_preferences", MODE_PRIVATE)
        Log.d("ActivityBuscar", "onCreate: SharedPreferences cargados.")

        // Configurar los spinners con los valores de arrays en los recursos
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

        Log.d("ActivityBuscar", "onCreate: Spinners configurados.")

        // Configurar el botón de búsqueda
        btnBuscar.setOnClickListener {

            Log.d("ActivityBuscar", "btnBuscar: Botón de búsqueda presionado.")

            // Obtener los valores seleccionados de los spinners y convertirlos a rangos
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

            // Crear el objeto JSON con los parámetros
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

            // Realizar la búsqueda enviando los parámetros
            realizarBusqueda(params)
        }
    }

    // Método para configurar los spinners con los valores de recursos
    private fun setupSpinner(spinner: Spinner, arrayResId: Int) {
        val adapter = ArrayAdapter.createFromResource(
            this,
            arrayResId,
            android.R.layout.simple_spinner_item
        )
        adapter.setDropDownViewResource(android.R.layout.simple_spinner_dropdown_item)
        spinner.adapter = adapter
    }

    // Método para convertir un valor de spinner a un rango de enteros
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

    // Método para realizar la solicitud HTTP a la API
    private fun realizarBusqueda(params: JSONObject) {

        val url = "https://model.cuspide.club/find_closest_actors" // Reemplazar con la URL de tu API

        // Obtener el token de sesión desde SharedPreferences
        val token = getTokenFromPreferences()

        if (token == null) {
            Log.e("ActivityBuscar", "realizarBusqueda: Token de sesión no encontrado.")
            Toast.makeText(this, "No se ha encontrado el token de sesión.", Toast.LENGTH_SHORT).show()
            return
        }

        Log.d("ActivityBuscar", "realizarBusqueda: Token de sesión encontrado.")

        val client = OkHttpClient()

        // Crear el cuerpo de la solicitud con el JSON de parámetros
        val requestBody = RequestBody.create("application/json".toMediaType(), params.toString())

        // Crear la solicitud con el encabezado de autorización
        val request = Request.Builder()
            .url(url)
            .post(requestBody)  // Usamos POST para la API
            .addHeader("Authorization", "Bearer $token")  // Agregar el token al encabezado
            .build()

        Log.d("ActivityBuscar", "realizarBusqueda: Solicitud enviada.")

        // Enviar la solicitud
        client.newCall(request).enqueue(object : Callback {
            override fun onFailure(call: Call, e: IOException) {
                Log.e("ActivityBuscar", "onFailure: Error en la búsqueda: ${e.message}")
                runOnUiThread {
                    Toast.makeText(this@ActivityBuscar, "Error en la búsqueda: ${e.message}", Toast.LENGTH_SHORT).show()
                }
            }



            override fun onResponse(call: Call, response: Response) {
                if (response.isSuccessful) {
                    val responseData = response.body?.string()
                    Log.d("ActivityBuscar", "Respuesta cruda de la API: $responseData")

                    if (responseData != null) {
                        try {
                            val jsonResponse = JSONObject(responseData)

                            // Verificar si el JSON contiene la clave "closest_indices"
                            if (jsonResponse.has("closest_indices")) {
                                val closestIndicesJsonArray = jsonResponse.getJSONArray("closest_indices")

                                // Limpiar la lista de closestIndices antes de agregar nuevos valores
                                val closestIndices = mutableListOf<Int>()
                                Log.d("ActivityBuscar", "closestIndices lista limpia: $closestIndices")

                                // Agregar los índices al array
                                for (i in 0 until closestIndicesJsonArray.length()) {
                                    val index = closestIndicesJsonArray.getInt(i)  // Obtener el valor entero
                                    closestIndices.add(index)
                                    Log.d("ActivityBuscar", "Índice agregado: $index")
                                }

                                // Guardar los índices en SharedPreferences como un Set<String> (puedes guardar como Set<Int> si lo prefieres)
                                sharedPreferences.edit().putStringSet("closest_indices", closestIndices.map { it.toString() }.toSet()).commit()

                                // Confirmar que los datos se han guardado en SharedPreferences
                                Log.d("ActivityBuscar", "closest_indices guardados en SharedPreferences: ${closestIndices.map { it.toString() }}")

                                // Verificar que los datos se han guardado correctamente
                                val savedIndices = sharedPreferences.getStringSet("closest_indices", emptySet())
                                Log.d("ActivityBuscar", "closest_indices recuperados de SharedPreferences: $savedIndices")

                            } else {
                                Log.e("ActivityBuscar", "La respuesta JSON no contiene closest_indices.")
                            }

                        } catch (e: Exception) {
                            Log.e("ActivityBuscar", "Error al parsear la respuesta: ${e.message}")
                        }
                    } else {
                        Log.e("ActivityBuscar", "responseData es null, no se pudo procesar la respuesta.")
                    }

                    runOnUiThread {
                        Toast.makeText(this@ActivityBuscar, "Búsqueda exitosa", Toast.LENGTH_SHORT).show()
                    }

                } else {
                    Log.e("ActivityBuscar", "onResponse: Error en la búsqueda")
                    runOnUiThread {
                        Toast.makeText(this@ActivityBuscar, "Error en la búsqueda", Toast.LENGTH_SHORT).show()
                    }
                }

                // Navegar a la actividad de resultados
                Log.d("ActivityBuscar", "Redirigiendo a ResultadoActivity.")
                val intent = Intent(this@ActivityBuscar, ResultadoActivity::class.java)
                startActivity(intent)
            }
        })
    }

    // Obtener el token de sesión desde SharedPreferences
    private fun getTokenFromPreferences(): String? {
        return sharedPreferences.getString("token", null)
    }
}
