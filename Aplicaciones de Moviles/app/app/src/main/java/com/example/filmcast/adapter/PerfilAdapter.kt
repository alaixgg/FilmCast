package com.example.filmcast.adapter

import android.view.LayoutInflater
import android.view.ViewGroup
import androidx.recyclerview.widget.RecyclerView
import com.example.filmcast.Perfil
import com.example.filmcast.R

class PerfilAdapter (private val perfilList: List<Perfil>) : RecyclerView.Adapter<PerfilViewHolder>(){

    override fun onCreateViewHolder(parent: ViewGroup, viewType: Int): PerfilViewHolder {
        val layoutIflater = LayoutInflater.from(parent.context)
        return PerfilViewHolder(layoutIflater.inflate(R.layout.item_perfil, parent, false))
    }

    override fun getItemCount(): Int = perfilList.size

    override fun onBindViewHolder(holder: PerfilViewHolder, position: Int) {
        val item = perfilList[position]
        holder.render(item)
    }

}