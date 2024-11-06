package com.example.filmcast.ui.login

import android.os.Bundle
import androidx.appcompat.app.AppCompatActivity
import androidx.recyclerview.widget.LinearLayoutManager
import androidx.recyclerview.widget.RecyclerView
import com.example.filmcast.R
import com.example.filmcast.adapter.PerfilAdapter
import com.example.filmcast.recycler.ResultadoProvider

class ResultadoActivity : AppCompatActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_actores_resultado)
        initRecyclerView()
    }

    private fun initRecyclerView() {
        val recyclerView = findViewById<RecyclerView>(R.id.recyclerProfile)
        recyclerView.layoutManager = LinearLayoutManager(this)
        recyclerView.adapter = PerfilAdapter(ResultadoProvider.perfilList)
    }
}