package com.example.filmcast.adapter

import android.view.LayoutInflater
import android.view.ViewGroup
import androidx.recyclerview.widget.RecyclerView
import com.example.filmcast.R

class InfoPerfilAdapter(private val infoActorList: List<InfoPerfil>) : RecyclerView.Adapter<InfoActorViewHolder>() {

    // Se infla el layout de cada item y se crea el ViewHolder correspondiente
    override fun onCreateViewHolder(parent: ViewGroup, viewType: Int): InfoActorViewHolder {
        val layoutInflater = LayoutInflater.from(parent.context)
        val view = layoutInflater.inflate(R.layout.item_perfil, parent, false)
        return InfoActorViewHolder(view)
    }

    // Devolver el número de items en la lista
    override fun getItemCount(): Int = infoActorList.size

    // Asignar los datos de cada item en el ViewHolder
    override fun onBindViewHolder(holder: InfoActorViewHolder, position: Int) {
        val item = infoActorList[position]
        holder.render(item)
    }
}
