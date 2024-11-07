import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import android.widget.TextView
import androidx.recyclerview.widget.RecyclerView
import com.example.filmcast.R

class ActoresAdapter(
    private val actores: List<Map<String, Any>>,
    private val onClick: (Map<String, Any>) -> Unit
) : RecyclerView.Adapter<ActoresAdapter.ActorViewHolder>() {

    override fun onCreateViewHolder(parent: ViewGroup, viewType: Int): ActorViewHolder {
        val view = LayoutInflater.from(parent.context).inflate(R.layout.item_perfil, parent, false)
        return ActorViewHolder(view)
    }

    override fun onBindViewHolder(holder: ActorViewHolder, position: Int) {
        val actor = actores[position]
        holder.bind(actor)
    }

    override fun getItemCount(): Int = actores.size

    inner class ActorViewHolder(itemView: View) : RecyclerView.ViewHolder(itemView) {
        private val nombreTextView: TextView = itemView.findViewById(R.id.tv_nombre)


        fun bind(actor: Map<String, Any>) {
            nombreTextView.text = actor["nombre"] as String
            // Aquí puedes cargar la imagen con Glide, Picasso, o similar
            // Glide.with(itemView).load(actor["imagen"]).into(imagenImageView)

            itemView.setOnClickListener {
                onClick(actor)  // Llama al callback cuando se hace clic
            }
        }
    }
}
