package com.example.filmcast.ui.login

import android.app.DatePickerDialog
import android.os.Bundle
import android.widget.ArrayAdapter
import android.widget.TextView
import android.widget.Toast
import androidx.appcompat.app.AppCompatActivity
import androidx.lifecycle.lifecycleScope
import com.example.filmcast.R
import com.example.filmcast.databinding.ActivityCreaProyectoBinding
import kotlinx.coroutines.launch
import retrofit2.Retrofit
import retrofit2.converter.gson.GsonConverterFactory
import retrofit2.Response
import retrofit2.http.Body
import retrofit2.http.POST
import java.text.SimpleDateFormat
import java.util.*

class Crea_proyecto : AppCompatActivity() {

    private lateinit var binding: ActivityCreaProyectoBinding

    // Inicializar Retrofit
    private val retrofit by lazy {
        Retrofit.Builder()
            .baseUrl("https://cuspide.club")
            .addConverterFactory(GsonConverterFactory.create())
            .build()
    }


    private val apiService by lazy {
        retrofit.create(ApiService::class.java)
    }


    private val dateFormat = SimpleDateFormat("dd/MM/yyyy", Locale.getDefault())

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        binding = ActivityCreaProyectoBinding.inflate(layoutInflater)
        setContentView(binding.root)


        val actores = listOf("Actor 1", "Actor 2", "Actor 3")
        val spinnerAdapter = ArrayAdapter(this, android.R.layout.simple_spinner_item, actores)
        spinnerAdapter.setDropDownViewResource(android.R.layout.simple_spinner_dropdown_item)
        binding.BUSpinnerEducacion.adapter = spinnerAdapter


        binding.ProGuardarProyecto.setOnClickListener {
            val titulo = binding.ProNombreProyecto.text.toString()
            val descripcion = binding.ProDescripcionProyecto.text.toString()
            val genero = binding.ProGeneroCinematografico.text.toString()
            val fechaInicio = binding.ProFechaInicio.text.toString()
            val fechaFin = binding.ProFechaFin.text.toString()
            val presupuesto = binding.ProPresupuesto.text.toString().toDoubleOrNull()


            if (titulo.isNotBlank() && descripcion.isNotBlank() && genero.isNotBlank() &&
                fechaInicio.isNotBlank() && fechaFin.isNotBlank() && presupuesto != null) {

                val actorSeleccionado = binding.BUSpinnerEducacion.selectedItem.toString()

                val proyecto = mapOf(
                    "titulo" to titulo,
                    "descripcion" to descripcion,
                    "genero" to genero,
                    "fecha_inicio" to fechaInicio,
                    "fecha_fin" to fechaFin,
                    "presupuesto" to presupuesto,
                    "actores_seleccionados" to listOf(actorSeleccionado)
                )

                crearProyecto(proyecto)
            } else {
                Toast.makeText(this, "Por favor complete todos los campos", Toast.LENGTH_SHORT).show()
            }
        }

        binding.ProFechaInicio.setOnClickListener {
            showDatePickerDialog(binding.ProFechaInicio)
        }

        binding.ProFechaFin.setOnClickListener {
            showDatePickerDialog(binding.ProFechaFin)
        }
    }

    private fun showDatePickerDialog(textView: TextView) {
        val calendar = Calendar.getInstance()
        val datePickerDialog = DatePickerDialog(
            this,
            { _, year, monthOfYear, dayOfMonth ->
                calendar.set(year, monthOfYear, dayOfMonth)
                val selectedDate = dateFormat.format(calendar.time)
                textView.setText(selectedDate)
            },
            calendar.get(Calendar.YEAR),
            calendar.get(Calendar.MONTH),
            calendar.get(Calendar.DAY_OF_MONTH)
        )
        datePickerDialog.show()
    }

    private fun crearProyecto(proyecto: Map<String, Any>) {
        lifecycleScope.launch {
            try {
                val response: Response<ApiResponse> = apiService.crearProyecto(proyecto)
                if (response.isSuccessful) {
                    val message = response.body()?.message ?: "Proyecto creado con éxito"
                    Toast.makeText(this@Crea_proyecto, message, Toast.LENGTH_SHORT).show()
                } else {
                    val errorMessage = response.errorBody()?.string() ?: "Error al crear el proyecto"
                    Toast.makeText(this@Crea_proyecto, errorMessage, Toast.LENGTH_SHORT).show()
                }
            } catch (e: Exception) {
                Toast.makeText(this@Crea_proyecto, "Error: ${e.message}", Toast.LENGTH_SHORT).show()
            }
        }
    }

    interface ApiService {
        @POST("/crear_proyecto")
        suspend fun crearProyecto(
            @Body proyecto: Map<String, Any>
        ): Response<ApiResponse>
    }

    data class ApiResponse(val message: String)
}
