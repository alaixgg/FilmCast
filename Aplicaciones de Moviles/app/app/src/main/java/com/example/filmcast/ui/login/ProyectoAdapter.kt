import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import android.widget.TextView
import androidx.recyclerview.widget.RecyclerView
import com.example.filmcast.R

class ProyectoAdapter(private val proyectos: List<Proyecto>) : RecyclerView.Adapter<ProyectoAdapter.ProyectoViewHolder>() {

    override fun onCreateViewHolder(parent: ViewGroup, viewType: Int): ProyectoViewHolder {
        val view = LayoutInflater.from(parent.context).inflate(R.layout.item_proyecto, parent, false)
        return ProyectoViewHolder(view)
    }

    override fun onBindViewHolder(holder: ProyectoViewHolder, position: Int) {
        val proyecto = proyectos[position]
        holder.titulo.text = proyecto.titulo
        holder.fecha.text = proyecto.fecha
        holder.precio.text = proyecto.precio
        holder.genero.text = proyecto.genero
    }

    override fun getItemCount(): Int {
        return proyectos.size
    }

    class ProyectoViewHolder(view: View) : RecyclerView.ViewHolder(view) {
        val titulo: TextView = view.findViewById(R.id.LP_title)
        val fecha: TextView = view.findViewById(R.id.LP_participants)
        val precio: TextView = view.findViewById(R.id.LP_date)
        val genero: TextView = view.findViewById(R.id.LP_messages)
    }
}
