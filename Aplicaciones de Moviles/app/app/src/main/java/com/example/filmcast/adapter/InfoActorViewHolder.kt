package com.example.filmcast.adapter

import android.view.View
import android.widget.TextView
import androidx.recyclerview.widget.RecyclerView
import com.example.filmcast.R

class InfoActorViewHolder(view:View):RecyclerView.ViewHolder(view) {

    val infoNombre = view.findViewById<TextView>(R.id.Rc_nombre)
    val infoGenero = view.findViewById<TextView>(R.id.Rc_genero)
    val infoPrecio = view.findViewById<TextView>(R.id.Rc_precio)
    val infoFilm = view.findViewById<TextView>(R.id.Rc_genero_pelicula)

    fun render(infoPerfilModel: InfoPerfil) {
        infoNombre.text = infoPerfilModel.infoNombre
        infoGenero.text = infoPerfilModel.infoGenero
        infoPrecio.text = infoPerfilModel.infoPrecio
        infoFilm.text = infoPerfilModel.infoFilm
    }
}