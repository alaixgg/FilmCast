package com.example.filmcast.ui.login

import android.os.Bundle
import android.widget.Button
import android.widget.EditText
import androidx.appcompat.app.AppCompatActivity
import com.example.filmcast.R
import com.example.filmcast.data.RetroFit.PerfilRequest
import retrofit2.Retrofit
import retrofit2.converter.gson.GsonConverterFactory

class EditarPerfil : AppCompatActivity() {

    private val retrofit by lazy {
        Retrofit.Builder()
            .baseUrl("https://api.example.com/") // Cambia esto a la URL base de tu API
            .addConverterFactory(GsonConverterFactory.create())
            .build()
    }



    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_editar_perfil)


        val cancelarButton = findViewById<Button>(R.id.EDP_Cancelar)
        cancelarButton.setOnClickListener {
            finish()
        }


        val guardarButton = findViewById<Button>(R.id.EDP_Guardar)
        guardarButton.setOnClickListener {
            enviarDatos()
        }
    }

    private fun enviarDatos() {

        val nombre = findViewById<EditText>(R.id.EDP_Nombre_txt).text.toString()
        val descripcion = findViewById<EditText>(R.id.EDP_Descripcion_tx).text.toString()
        val telefono = findViewById<EditText>(R.id.EDP_Telefono_tx).text.toString()
        val nacionalidad = findViewById<EditText>(R.id.EDP_Nacionalidad_tx).text.toString()
        val email = findViewById<EditText>(R.id.EDP_Email_tx).text.toString()


        val perfilRequest = PerfilRequest(nombre, descripcion, telefono, nacionalidad, email)



    }
}
