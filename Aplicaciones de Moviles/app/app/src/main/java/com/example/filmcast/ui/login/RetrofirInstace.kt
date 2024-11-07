package com.example.filmcast.ui.login

import retrofit2.Retrofit
import retrofit2.converter.gson.GsonConverterFactory

object RetrofirInstace {
    private const val BASE_URL = "https://db.cuspide.club"

    val api: ActorApiService by lazy {
        Retrofit.Builder()
            .baseUrl(BASE_URL)
            .addConverterFactory(GsonConverterFactory.create())
            .build()
            .create(ActorApiService::class.java)
    }
}