import android.os.Bundle
import android.widget.Toast
import androidx.appcompat.app.AppCompatActivity
import androidx.recyclerview.widget.LinearLayoutManager
import androidx.recyclerview.widget.RecyclerView
import com.example.filmcast.R
import retrofit2.Call
import retrofit2.Callback
import retrofit2.Response
import retrofit2.Retrofit
import retrofit2.converter.gson.GsonConverterFactory
import retrofit2.http.GET
import retrofit2.http.Header

// Definimos la interfaz Retrofit
interface ApiService {
    @GET("mis_proyectos")
    fun obtenerProyectos(@Header("Authorization") token: String): Call<List<Proyecto>>
}

// Clase de datos para Proyecto
data class Proyecto(val titulo: String, val fecha: String, val precio: String, val genero: String)

class Lista_proyectActivity : AppCompatActivity() {

    private lateinit var recyclerView: RecyclerView
    private lateinit var proyectoAdapter: ProyectoAdapter
    private val proyectosUnicos = mutableListOf<Proyecto>()
    private var token: String? = null  // Token de sesión (se debe obtener del almacenamiento local)

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_lista_proyect)

        recyclerView = findViewById(R.id.recyclerProfile)
        recyclerView.layoutManager = LinearLayoutManager(this)

        // Creamos el adaptador y lo asociamos al RecyclerView
        proyectoAdapter = ProyectoAdapter(proyectosUnicos)
        recyclerView.adapter = proyectoAdapter

        // Obtener el token desde SharedPreferences (o desde donde lo tengas)
        token = getSharedPreferences("MiApp", MODE_PRIVATE).getString("token", null)

        // Si el token no es nulo, realizamos la solicitud para obtener los proyectos
        if (token != null) {
            obtenerProyectos()
        } else {
            // Si no hay token, mostramos un mensaje de error
            Toast.makeText(this, "No se encontró el token", Toast.LENGTH_SHORT).show()
        }
    }

    private fun obtenerProyectos() {
        val retrofit = Retrofit.Builder()
            .baseUrl("https://db.cuspide.club/")  // Base URL de la API
            .addConverterFactory(GsonConverterFactory.create())
            .build()

        val apiService = retrofit.create(ApiService::class.java)

        // Realizamos la llamada GET con el token de autenticación
        val call = apiService.obtenerProyectos("Bearer $token")

        call.enqueue(object : Callback<List<Proyecto>> {
            override fun onResponse(call: Call<List<Proyecto>>, response: Response<List<Proyecto>>) {
                if (response.isSuccessful && response.body() != null) {
                    val proyectos = response.body()!!

                    // Filtrar los proyectos para obtener solo los títulos únicos
                    val titulosVistos = mutableSetOf<String>()
                    val proyectosFiltrados = proyectos.filter { proyecto ->
                        if (!titulosVistos.contains(proyecto.titulo)) {
                            titulosVistos.add(proyecto.titulo)
                            true
                        } else {
                            false
                        }
                    }

                    // Actualizamos la lista de proyectos
                    proyectosUnicos.clear()
                    proyectosUnicos.addAll(proyectosFiltrados)

                    // Notificamos al adaptador que los datos han cambiado
                    proyectoAdapter.notifyDataSetChanged()
                } else {
                    // Si la respuesta no es exitosa, mostramos un mensaje
                    Toast.makeText(this@Lista_proyectActivity, "Error al obtener los proyectos", Toast.LENGTH_SHORT).show()
                }
            }

            override fun onFailure(call: Call<List<Proyecto>>, t: Throwable) {
                // Si falla la solicitud, mostramos un mensaje de error
                Toast.makeText(this@Lista_proyectActivity, "Error en la conexión", Toast.LENGTH_SHORT).show()
            }
        })
    }
}
