package com.example.filmcast.ui.login

import android.content.Context
import android.os.Bundle
import android.util.Log
import android.widget.Button
import android.widget.EditText
import android.widget.Toast
import androidx.appcompat.app.AppCompatActivity
import com.example.filmcast.R
import okhttp3.*
import okhttp3.MediaType.Companion.toMediaType
import org.json.JSONObject
import java.io.IOException

class EditarPerfil : AppCompatActivity() {

    private lateinit var btnGuardar: Button
    private lateinit var etTelefono: EditText
    private lateinit var etEmail: EditText
    private lateinit var etDescripcion: EditText
    private lateinit var etNacionalidad: EditText
    private lateinit var token: String

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_editar_perfil)

        btnGuardar = findViewById(R.id.EDP_Guardar)
        etTelefono = findViewById(R.id.EDP_Telefono_tx)
        etEmail = findViewById(R.id.EDP_Email_tx)
        etDescripcion = findViewById(R.id.EDP_Descripcion_tx)
        etNacionalidad = findViewById(R.id.EDP_Nacionalidad_tx)

        token = getTokenFromPreferences()

        if (token.isNullOrEmpty()) {
            Toast.makeText(this, "Token no disponible. Inicia sesión nuevamente.", Toast.LENGTH_SHORT).show()
            return
        }

        obtenerPerfil(token)

        btnGuardar.setOnClickListener {
            val telefono = etTelefono.text.toString()
            val email = etEmail.text.toString()
            val descripcion = etDescripcion.text.toString()
            val nacionalidad = etNacionalidad.text.toString()

            actualizarPerfil(token, telefono, email, descripcion, nacionalidad)
        }

    }

    private fun getTokenFromPreferences(): String {
        val sharedPreferences = getSharedPreferences("app_preferences", Context.MODE_PRIVATE)
        return sharedPreferences.getString("token", "") ?: ""

        Log.d("PerfilActivity", "Token recuperado: $token")
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
                    Toast.makeText(this@EditarPerfil, "Error al obtener los datos del perfil", Toast.LENGTH_SHORT).show()
                }
            }

            override fun onResponse(call: Call, response: Response) {
                if (response.isSuccessful) {
                    val responseData = response.body?.string()
                    try {
                        val jsonObject = JSONObject(responseData)

                        val pais = jsonObject.optString("Pais", "")
                        Log.d("EditarPerfil", "Pais recibido: $pais")

                        runOnUiThread {
                            etTelefono.setText(jsonObject.optString("telefono", ""))
                            etEmail.setText(jsonObject.optString("email", ""))
                            etDescripcion.setText(jsonObject.optString("descripcion", ""))
                            etNacionalidad.setText(jsonObject.optString("nacionalidad",""))

                            Log.d("PerfilActivity", "nacionalidad: ${jsonObject.optString("nacionalidad", "Campo no encontrado")}")

                        }
                    } catch (e: Exception) {
                        runOnUiThread {
                            Toast.makeText(this@EditarPerfil, "Error al procesar los datos del perfil", Toast.LENGTH_SHORT).show()
                        }
                    }
                } else {
                    runOnUiThread {
                        Toast.makeText(this@EditarPerfil, "Error al cargar perfil", Toast.LENGTH_SHORT).show()
                    }
                }
            }
        })
    }


    private fun actualizarPerfil(token: String, telefono: String, email: String, descripcion: String, nacionalidad: String) {
        val url = "https://db.cuspide.club/editar_perfil"

        val payload = JSONObject().apply {
            put("telefono", telefono)
            put("email", email)
            put("descripcion", descripcion)
            put("Pais", nacionalidad)

            Log.d("PerfilActivity", "Nacionalidad: $nacionalidad")  // Verifica qué se está recuperando

        }

        val client = OkHttpClient()
        val requestBody = RequestBody.create("application/json".toMediaType(), payload.toString())
        val request = Request.Builder()
            .url(url)
            .header("Authorization", "Bearer $token")
            .post(requestBody)
            .build()

        client.newCall(request).enqueue(object : Callback {
            override fun onFailure(call: Call, e: IOException) {
                runOnUiThread {
                    Toast.makeText(this@EditarPerfil, "Error al actualizar el perfil", Toast.LENGTH_SHORT).show()
                }
            }

            override fun onResponse(call: Call, response: Response) {
                if (response.isSuccessful) {
                    runOnUiThread {
                        Toast.makeText(this@EditarPerfil, "Perfil actualizado con éxito", Toast.LENGTH_SHORT).show()
                        finish() // Volver a la pantalla anterior
                    }
                } else {
                    runOnUiThread {
                        Toast.makeText(this@EditarPerfil, "Error al actualizar el perfil", Toast.LENGTH_SHORT).show()
                    }
                }
            }
        })
    }
}
