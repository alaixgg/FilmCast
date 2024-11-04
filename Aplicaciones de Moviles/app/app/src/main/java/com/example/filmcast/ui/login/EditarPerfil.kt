package com.example.filmcast

import android.os.Bundle
import com.example.filmcast.*
import android.widget.Toast
import androidx.appcompat.app.AppCompatActivity
import com.example.filmcast.databinding.ActivityEditarPerfilBinding
import retrofit2.Call
import retrofit2.Callback
import retrofit2.Response

class EditarPerfil : AppCompatActivity() {
    private lateinit var binding: ActivityEditarPerfilBinding
    private val token = "Bearer " + // Aquí debes obtener el token desde el almacenamiento seguro.

            override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        binding = ActivityEditarPerfilBinding.inflate(layoutInflater)
        setContentView(binding.root)

        cargarDatosPerfil()
        binding.EDPGuardar.setOnClickListener { actualizarPerfil() }
    }

    private fun cargarDatosPerfil() {
        apiService.obtenerPerfil(token).enqueue(object : Callback<UsuarioInfo> {
            override fun onResponse(call: Call<UsuarioInfo>, response: Response<UsuarioInfo>) {
                if (response.isSuccessful) {
                    val usuario = response.body()
                    usuario?.let {
                        binding.EDPNombreTxt.setText(it.nombre) // Solo para visualización
                        binding.EDPDescripcionTx.setText(it.descripcion)
                        binding.EDPTelefonoTx.setText(it.telefono)
                        binding.EDPNacionalidadTx.setText(it.Pais)
                        binding.EDPEmailTx.setText(it.email)
                    }
                } else {
                    Toast.makeText(this@EditarPerfil, "Error al cargar el perfil", Toast.LENGTH_SHORT).show()
                }
            }

            override fun onFailure(call: Call<UsuarioInfo>, t: Throwable) {
                Toast.makeText(this@EditarPerfil, "Error de conexión", Toast.LENGTH_SHORT).show()
            }
        })
    }

    private fun actualizarPerfil() {
        val datosPerfil = PerfilEditData(
            telefono = binding.EDPTelefonoTx.text.toString(),
            email = binding.EDPEmailTx.text.toString(),
            descripcion = binding.EDPDescripcionTx.text.toString(),
            Pais = binding.EDPNacionalidadTx.text.toString()
        )

        apiService.editarPerfil(token, datosPerfil).enqueue(object : Callback<RespuestaEditarPerfil> {
            override fun onResponse(call: Call<RespuestaEditarPerfil>, response: Response<RespuestaEditarPerfil>) {
                if (response.isSuccessful) {
                    val resultado = response.body()
                    if (resultado?.success == true) {
                        Toast.makeText(this@EditarPerfil, "Perfil actualizado exitosamente", Toast.LENGTH_SHORT).show()
                        finish()
                    } else {
                        Toast.makeText(this@EditarPerfil, "Error: ${resultado?.message}", Toast.LENGTH_SHORT).show()
                    }
                } else {
                    Toast.makeText(this@EditarPerfil, "Error al actualizar el perfil", Toast.LENGTH_SHORT).show()
                }
            }

            override fun onFailure(call: Call<RespuestaEditarPerfil>, t: Throwable) {
                Toast.makeText(this@EditarPerfil, "Error de conexión", Toast.LENGTH_SHORT).show()
            }
        })
    }
}
