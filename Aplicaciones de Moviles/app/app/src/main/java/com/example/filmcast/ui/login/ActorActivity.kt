package com.example.filmcast.ui.login

import android.os.Bundle
import android.widget.TextView
import android.widget.Toast
import androidx.activity.ComponentActivity
import com.example.filmcast.R
import retrofit2.Call
import retrofit2.Callback
import retrofit2.Response
import retrofit2.Retrofit
import retrofit2.converter.gson.GsonConverterFactory
import retrofit2.http.GET
import retrofit2.http.Path

class ActorActivity : ComponentActivity() {

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_perfil)

        val actorId = 1 // Este valor puede cambiar dinámicamente, por ejemplo, a través de un Intent

        // Referencias a los TextViews
        val actorNameTextView: TextView = findViewById(R.id.Pe_titulo)
        val actorEmailTextView: TextView = findViewById(R.id.Pe_email)
        val actorPhoneTextView: TextView = findViewById(R.id.Pe_telefono)
        val actorNationalityTextView: TextView = findViewById(R.id.Pe_nacionalidad)
        val actorGenderTextView: TextView = findViewById(R.id.Pe_genero)
        val actorDescriptionTextView: TextView = findViewById(R.id.Pe_descripcion)


        getActorInfo(actorId, actorNameTextView, actorEmailTextView, actorPhoneTextView, actorNationalityTextView, actorGenderTextView, actorDescriptionTextView)
    }


    private fun getActorInfo(
        actorId: Int,
        nameTextView: TextView,
        emailTextView: TextView,
        phoneTextView: TextView,
        nationalityTextView: TextView,
        genderTextView: TextView,
        descriptionTextView: TextView
    ) {

        val retrofit = Retrofit.Builder()
            .baseUrl("https://yourapi.com/")
            .addConverterFactory(GsonConverterFactory.create())
            .build()


        val api = retrofit.create(ActorApi::class.java)


        val call = api.getActorInfo(actorId)


        call.enqueue(object : Callback<ActorResponse> {
            override fun onResponse(call: Call<ActorResponse>, response: Response<ActorResponse>) {
                if (response.isSuccessful && response.body() != null) {
                    val actor = response.body()!!


                    nameTextView.text = actor.name
                    emailTextView.text = actor.email
                    phoneTextView.text = actor.phone
                    nationalityTextView.text = actor.nationality
                    genderTextView.text = actor.gender
                    descriptionTextView.text = actor.description
                } else {

                    Toast.makeText(this@ActorActivity, "Error al obtener los datos del actor", Toast.LENGTH_SHORT).show()
                }
            }

            override fun onFailure(call: Call<ActorResponse>, t: Throwable) {

                Toast.makeText(this@ActorActivity, "Error de red: ${t.message}", Toast.LENGTH_SHORT).show()
            }
        })
    }


    interface ActorApi {
        @GET("info_actor/{actor_id}")
        fun getActorInfo(@Path("actor_id") actorId: Int): Call<ActorResponse>
    }


    data class ActorResponse(
        val id: Int,
        val name: String,
        val email: String,
        val phone: String,
        val nationality: String,
        val gender: String,
        val description: String
    )
}
