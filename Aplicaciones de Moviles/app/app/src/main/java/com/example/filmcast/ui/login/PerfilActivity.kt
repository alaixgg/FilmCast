package com.example.filmcast.ui.login

import android.content.Intent
import android.os.Bundle
import android.util.Log
import android.widget.Button
import android.widget.ImageView
import android.widget.TextView
import android.widget.Toast
import androidx.appcompat.app.AppCompatActivity
import com.example.filmcast.R
import okhttp3.*
import org.json.JSONObject
import java.io.IOException

class PerfilActivity : AppCompatActivity() {


    private lateinit var tvEmail: TextView
    private lateinit var tvTelefono: TextView
    private lateinit var tvDescripcion: TextView
    private lateinit var tvNacionalidad: TextView
    private lateinit var btnCerrarSesion: Button
    private lateinit var btnEditarPerfil: Button
    private lateinit var imgMenu: ImageView

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_perfil)



        tvEmail = findViewById(R.id.Pe_email)
        tvTelefono = findViewById(R.id.Pe_telefono)
        tvDescripcion = findViewById(R.id.Pe_descripcion)
        tvNacionalidad = findViewById(R.id.Pe_nacionalidad)
        btnCerrarSesion = findViewById(R.id.pe_cerrarSesiom)
        btnEditarPerfil = findViewById(R.id.pe_editar_perfil)
        imgMenu = findViewById(R.id.Pe_menu)

        val token = getTokenFromPreferences()



        if (token != null) {
            obtenerPerfil(token)
        } else {
            Toast.makeText(this, "No se ha encontrado el token de sesión.", Toast.LENGTH_SHORT).show()
        }

        btnEditarPerfil.setOnClickListener {
            val intent = Intent(this, EditarPerfil::class.java)
            startActivity(intent)
        }

        btnCerrarSesion.setOnClickListener {
            cerrarSesion()
        }

        imgMenu.setOnClickListener {
            val intent = Intent(this, MenuActivity::class.java)
            startActivity(intent)
        }
    }

    private fun obtenerPerfil(token: String) {
        val url = "https://db.cuspide.club/perfil"

        val client = OkHttpClient()
        val request = Request.Builder()
            .url(url)
            .header("Authorization", "Bearer $token")
            .build()

        client.newCall(request).enqueue(object : Callback {
            override fun onFailure(call: Call, e: IOException) {
                runOnUiThread {
                    Toast.makeText(this@PerfilActivity, "Error: ${e.message}", Toast.LENGTH_SHORT).show()
                }
            }

            override fun onResponse(call: Call, response: Response) {
                if (response.isSuccessful) {
                    val responseData = response.body?.string()
                    val jsonObject = JSONObject(responseData)

                    val email = jsonObject.optString("email", "No disponible")
                    val telefono = jsonObject.optString("telefono", "No disponible")
                    val descripcion = jsonObject.optString("descripcion", "No disponible")
                    val nacionalidad = jsonObject.optString("nacionalidad", "No disponible")

                    runOnUiThread {

                        tvEmail.text = email
                        tvTelefono.text = telefono
                        tvDescripcion.text = descripcion
                        tvNacionalidad.text = nacionalidad
                    }
                } else {
                    runOnUiThread {
                        Toast.makeText(this@PerfilActivity, "Error al obtener el perfil.", Toast.LENGTH_SHORT).show()
                    }
                }
            }
        })
    }

    private fun getTokenFromPreferences(): String? {
        val sharedPreferences = getSharedPreferences("app_preferences", MODE_PRIVATE)
        val token = sharedPreferences.getString("token", null)

        Log.d("PerfilActivity", "Token recuperado: $token")

        return token
    }

    private fun cerrarSesion() {
        val sharedPreferences = getSharedPreferences("app_preferences", MODE_PRIVATE)
        with(sharedPreferences.edit()) {
            remove("token") // Elimina el token
            apply()
        }
        val intent = Intent(this, LoginActivity::class.java)
        startActivity(intent)
        finish()
    }
}