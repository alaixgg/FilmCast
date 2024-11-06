import android.os.Bundle
import android.widget.TextView
import android.widget.Toast
import androidx.appcompat.app.AppCompatActivity
import com.example.filmcast.R
import retrofit2.Call
import retrofit2.Callback
import retrofit2.Response
import retrofit2.Retrofit
import retrofit2.converter.gson.GsonConverterFactory
import retrofit2.http.GET
import retrofit2.http.Path

class Proyectos : AppCompatActivity() {

    private lateinit var tvNombre: TextView
    private lateinit var tvDescripcion: TextView
    private lateinit var tvGenero: TextView
    private lateinit var tvFechaInicio: TextView
    private lateinit var tvFechaFin: TextView
    private lateinit var tvPresupuesto: TextView

    private val BASE_URL = "https://db.cuspide.club/mis_proyectos"  // Cambia por la URL base de tu API

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_proyectos)


        tvDescripcion = findViewById(R.id.Pr_descripcion_proyecto_re)
        tvGenero = findViewById(R.id.PA_genero_cine_tx)
        tvFechaInicio = findViewById(R.id.Pr_fecha_inicio_r)
        tvFechaFin = findViewById(R.id.Pr_fecha_fin_r)
        tvPresupuesto = findViewById(R.id.Pr_presupuesto_r)


        val proyectoId = intent.getIntExtra("proyecto_id", 0)


        val retrofit = Retrofit.Builder()
            .baseUrl(BASE_URL)
            .addConverterFactory(GsonConverterFactory.create())
            .build()

        val apiService = retrofit.create(ApiService::class.java)

        val call = apiService.getProyecto(proyectoId)
        call.enqueue(object : Callback<Proyecto> {
            override fun onResponse(call: Call<Proyecto>, response: Response<Proyecto>) {
                if (response.isSuccessful && response.body() != null) {
                    actualizarUI(response.body()!!)  // Llamamos a la función para actualizar la UI
                } else {
                    Toast.makeText(this@Proyectos, "Error en la respuesta", Toast.LENGTH_SHORT).show()
                }
            }

            override fun onFailure(call: Call<Proyecto>, t: Throwable) {
                Toast.makeText(this@Proyectos, "Error de red: ${t.message}", Toast.LENGTH_LONG).show()
            }
        })
    }

    private fun actualizarUI(proyecto: Proyecto) {
        tvNombre.text = proyecto.nombre
        tvDescripcion.text = proyecto.descripcion
        tvGenero.text = proyecto.generoCine
        tvFechaInicio.text = proyecto.fechaInicio
        tvFechaFin.text = proyecto.fechaFin
        tvPresupuesto.text = proyecto.presupuesto
    }

    interface ApiService {
        @GET("info_proyecto/{proyecto_id}")
        fun getProyecto(@Path("proyecto_id") proyectoId: Int): Call<Proyecto>
    }

    data class Proyecto(
        val nombre: String,
        val descripcion: String,
        val generoCine: String,
        val fechaInicio: String,
        val fechaFin: String,
        val presupuesto: String
    )
}
