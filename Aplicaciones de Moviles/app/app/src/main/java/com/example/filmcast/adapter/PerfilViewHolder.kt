package com.example.filmcast.adapter

import android.view.View
import android.widget.ImageView
import android.widget.TextView
import androidx.recyclerview.widget.RecyclerView
import com.example.filmcast.Perfil
import com.example.filmcast.R

class PerfilViewHolder(view: View): RecyclerView.ViewHolder(view) {

    val nombre = view.findViewById<TextView>(R.id.tv_nombre)
    val genero = view.findViewById<TextView>(R.id.tv_genero)
    val precio = view.findViewById<TextView>(R.id.tv_precio)
    val generoCine = view.findViewById<TextView>(R.id.tv_genero_pelicula)
    val foto = view.findViewById<ImageView>(R.id.iv_perfil)

    fun render(perfil: Perfil){
        nombre.text = perfil.nombre
        genero.text = perfil.genero
        precio.text = perfil.precio
        generoCine.text = perfil.generoCine
    }
}