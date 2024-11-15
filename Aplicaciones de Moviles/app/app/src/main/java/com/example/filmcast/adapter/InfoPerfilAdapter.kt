package com.example.filmcast.adapter

import android.view.LayoutInflater
import android.view.ViewGroup
import androidx.recyclerview.widget.RecyclerView
import com.example.filmcast.R

class InfoPerfilAdapter(private val infoActorList: List<InfoPerfil>) : RecyclerView.Adapter<InfoActorViewHolder>() {

    override fun onCreateViewHolder(parent: ViewGroup, viewType: Int): InfoActorViewHolder {
        val layoutInflater = LayoutInflater.from(parent.context)
        val view = layoutInflater.inflate(R.layout.item_perfil, parent, false)
        return InfoActorViewHolder(view)
    }

    override fun getItemCount(): Int = infoActorList.size

    override fun onBindViewHolder(holder: InfoActorViewHolder, position: Int) {
        val item = infoActorList[position]
        holder.render(item)
    }
}