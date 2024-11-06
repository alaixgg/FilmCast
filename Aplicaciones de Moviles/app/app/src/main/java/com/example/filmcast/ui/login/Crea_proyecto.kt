package com.example.filmcast.ui.login

import android.content.Intent
import android.os.Bundle
import android.widget.ImageView
import android.widget.Toast
import androidx.appcompat.app.AppCompatActivity
import com.example.filmcast.R

import com.example.filmcast.databinding.ActivityCreaProyectoBinding
import retrofit2.Retrofit
import retrofit2.converter.gson.GsonConverterFactory

class Crea_proyecto : AppCompatActivity() {

    private lateinit var binding: ActivityCreaProyectoBinding

    // Inicializa Retrofit y ApiService
    private val retrofit by lazy {
        Retrofit.Builder()
            .baseUrl("https://api.example.com/")
            .addConverterFactory(GsonConverterFactory.create())
            .build()
    }



}