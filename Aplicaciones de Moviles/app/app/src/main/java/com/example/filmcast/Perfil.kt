package com.example.filmcast

import retrofit2.Call
import retrofit2.http.Body
import retrofit2.http.GET
import retrofit2.http.Header
import retrofit2.http.POST
import retrofit2.http.Query

interface Perfil {
    @GET(Constants.PERFIL)
    fun obtenerPerfil(@Header("Authorization") token: String): Call<UsuarioInfo>


    @POST(Constants.EDITAR_PERFIL)
    fun editarPerfil(
        @Header("Authorization") token: String,
        @Body datosPerfil: PerfilEditData
    ): Call<RespuestaEditarPerfil>

}
