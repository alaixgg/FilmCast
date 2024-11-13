package com.example.filmcast.adapter

import android.view.LayoutInflater
import android.view.ViewGroup
import androidx.recyclerview.widget.RecyclerView
import com.example.filmcast.R

class InfoPerfilAdapter(private val InfoActorList:List<InfoPerfil> ) : RecyclerView.Adapter<InfoActorViewHolder>() {

    override fun onCreateViewHolder(parent: ViewGroup, viewType: Int): InfoActorViewHolder {
        val layoutInflater = LayoutInflater.from(parent.context)
        return InfoActorViewHolder(layoutInflater.inflate(R.layout.item_perfil, parent, false))

    }

    override fun getItemCount(): Int = InfoActorList.size

    override fun onBindViewHolder(holder: InfoActorViewHolder, position: Int) {
        val item = InfoActorList[position]
        holder.render(item)

    }
}