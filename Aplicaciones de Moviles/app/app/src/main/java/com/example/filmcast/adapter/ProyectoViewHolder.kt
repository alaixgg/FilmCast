package com.example.filmcast.adapter

import android.view.View
import android.widget.TextView
import androidx.recyclerview.widget.RecyclerView
import com.example.filmcast.R
import com.example.filmcast.recycler.Proyecto

class ProyectoViewHolder(view: View): RecyclerView.ViewHolder(view){

    val tituloProyecto = view.findViewById<TextView>(R.id.tv_titulo_proyecto)
    val fecha = view.findViewById<TextView>(R.id.tv_fecha)
    val ubicacion = view.findViewById<TextView>(R.id.iv_ubicacion)
    val mensaje = view.findViewById<TextView>(R.id.tv_mensaje)

    fun render(proyecto: Proyecto){
        tituloProyecto.text = proyecto.tituloProyecto
        fecha.text = proyecto.fecha
        ubicacion.text = proyecto.ubicacion
        mensaje.text = proyecto.mensaje
    }
}