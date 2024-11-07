package com.example.filmcast.ui.login

import retrofit2.Call
import retrofit2.http.GET
import retrofit2.http.Header
import retrofit2.http.Path

interface ActorApiService {
    @GET("info_actor/{actor_id")
    fun getActorInfo(@Path("actor_id") actorId: Int,
                     @Header("Authorization") token: String
    ):Call<ActorInfoResponse>
}