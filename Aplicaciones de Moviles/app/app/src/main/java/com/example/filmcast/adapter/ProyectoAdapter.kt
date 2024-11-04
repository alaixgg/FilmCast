package com.example.filmcast.adapter

import android.view.LayoutInflater
import android.view.ViewGroup
import androidx.recyclerview.widget.RecyclerView
import com.example.filmcast.R
import com.example.filmcast.recycler.Proyecto

class ProyectoAdapter (private val proyectosList: List<Proyecto>) : RecyclerView.Adapter<ProyectoViewHolder>(){
    override fun onCreateViewHolder(parent: ViewGroup, viewType: Int): ProyectoViewHolder {
        val layoutInflater = LayoutInflater.from(parent.context)
        return ProyectoViewHolder(layoutInflater.inflate(R.layout.item_proyecto, parent, false))
    }

    override fun getItemCount(): Int = proyectosList.size

    override fun onBindViewHolder(holder: ProyectoViewHolder, position: Int) {
        val item = proyectosList[position]
        holder.render(item)
    }


}