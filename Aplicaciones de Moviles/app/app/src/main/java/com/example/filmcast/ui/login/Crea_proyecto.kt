package com.example.filmcast.ui.login

import android.os.Bundle

import android.widget.Toast
import androidx.appcompat.app.AppCompatActivity
import com.example.filmcast.databinding.ActivityCreaProyectoBinding
import retrofit2.Call
import retrofit2.Callback
import retrofit2.Response

class Crea_proyecto : AppCompatActivity() {

    private lateinit var binding: ActivityCreaProyectoBinding

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        binding = ActivityCreaProyectoBinding.inflate(layoutInflater)
        setContentView(binding.root)

        binding.ProGuardarProyecto.setOnClickListener {
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

                guardarProyecto(proyecto)
            } else {
                Toast.makeText(this, "Por favor, completa todos los campos", Toast.LENGTH_SHORT).show()
            }
        }
    }

    private fun guardarProyecto(proyecto: Proyecto) {
        val call = ApiClient.apiService.crearProyecto(proyecto)
        call.enqueue(object : Callback<Void> {
            override fun onResponse(call: Call<Void>, response: Response<Void>) {
                if (response.isSuccessful) {
                    Toast.makeText(this@Crea_proyecto, "Proyecto guardado", Toast.LENGTH_SHORT).show()
                    finish()
                } else {
                    Toast.makeText(this@Crea_proyecto, "Error al guardar", Toast.LENGTH_SHORT).show()
                }
            }

            override fun onFailure(call: Call<Void>, t: Throwable) {
                Toast.makeText(this@Crea_proyecto, "Error de red", Toast.LENGTH_SHORT).show()
            }
        })
    }
}
