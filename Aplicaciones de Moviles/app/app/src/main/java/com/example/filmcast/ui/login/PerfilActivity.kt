package com.example.filmcast.ui.login

import android.os.Bundle
import android.widget.Toast
import androidx.appcompat.app.AppCompatActivity
import com.example.filmcast.Constants
import com.example.filmcast.Perfil
import com.example.filmcast.UsuarioInfo
import com.example.filmcast.databinding.ActivityPerfilBinding
import okhttp3.OkHttpClient
import okhttp3.logging.HttpLoggingInterceptor
import retrofit2.Call
import retrofit2.Callback
import retrofit2.Response
import retrofit2.Retrofit
import retrofit2.converter.gson.GsonConverterFactory


class PerfilActivity : AppCompatActivity() {

    private lateinit var binding: ActivityPerfilBinding

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        binding = ActivityPerfilBinding.inflate(layoutInflater)
        setContentView(binding.root)

        val token = "Bearer TU_TOKEN_AQUI"  // Reemplaza con el token de autenticación
        obtenerPerfil(token)
    }

    private fun obtenerPerfil(token: String) {
        // Configura Retrofit
        val logging = HttpLoggingInterceptor().apply { level = HttpLoggingInterceptor.Level.BODY }
        val client = OkHttpClient.Builder().addInterceptor(logging).build()

        val retrofit = Retrofit.Builder()
            .baseUrl(Constants.BASE_URL)
            .client(client)
            .addConverterFactory(GsonConverterFactory.create())
            .build()

        val perfilService = retrofit.create(Perfil::class.java)
        val call = perfilService.obtenerPerfil(token)

        // Realiza la llamada a la API
        call.enqueue(object : Callback<UsuarioInfo> {
            override fun onResponse(call: Call<UsuarioInfo>, response: Response<UsuarioInfo>) {
                if (response.isSuccessful) {
                    val usuarioInfo = response.body()
                    if (usuarioInfo != null) {
                        mostrarDatosPerfil(usuarioInfo)
                    }
                } else {
                    Toast.makeText(this@PerfilActivity, "Error al obtener el perfil", Toast.LENGTH_LONG).show()
                }
            }

            override fun onFailure(call: Call<UsuarioInfo>, t: Throwable) {
                Toast.makeText(this@PerfilActivity, "Error de red: ${t.message}", Toast.LENGTH_LONG).show()
            }
        })
    }

    private fun mostrarDatosPerfil(usuarioInfo: UsuarioInfo) {
        binding.PeNombre.text = usuarioInfo.id
        binding.PeEmail.text = usuarioInfo.email
        binding.PeTelefono.text = usuarioInfo.telefono
        binding.PeDescripcion.text = usuarioInfo.descripcion
        binding.PeNacionalidad.text = usuarioInfo.nacionalidad
    }
}
