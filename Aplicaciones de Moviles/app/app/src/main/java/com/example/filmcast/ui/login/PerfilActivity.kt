package com.example.filmcast.ui.login

<<<<<<<< HEAD:Aplicaciones de Moviles/app/app/src/main/java/com/example/filmcast/ui/login/menuActivity.kt
import android.content.Intent
import android.os.Bundle
import android.widget.Button
import android.widget.ImageView
========
import android.os.Bundle
>>>>>>>> refs/remotes/origin/Alejandro:Aplicaciones de Moviles/app/app/src/main/java/com/example/filmcast/ui/login/PerfilActivity.kt
import androidx.activity.enableEdgeToEdge
import androidx.appcompat.app.AppCompatActivity
import com.example.filmcast.R

<<<<<<<< HEAD:Aplicaciones de Moviles/app/app/src/main/java/com/example/filmcast/ui/login/menuActivity.kt
class menuActivity : AppCompatActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        enableEdgeToEdge()
        setContentView(R.layout.activity_menu)

        val menu_perfil = findViewById<ImageView>(R.id.menu_titulo_perfil)
        menu_perfil.setOnClickListener {
            val intent = Intent(this, PerfilActivity::class.java)
            startActivity(intent)
        }
        val menu_buscar = findViewById<Button>(R.id.menu_button_buscar)
        menu_buscar.setOnClickListener {
            val intent = Intent(this, ActivityBuscar::class.java)
            startActivity(intent)
        }
        val menu_guardados = findViewById<Button>(R.id.menu_button_guardados)
        menu_guardados.setOnClickListener {
            val intent = Intent(this, GuardadosActivity::class.java)
            startActivity(intent)
        }
        val menu_nuevo_proyecto =findViewById<Button>(R.id.nuv_proyecto)
        menu_nuevo_proyecto.setOnClickListener{
            val intent= Intent(this,Crea_proyecto::class.java)
            startActivity(intent)
        }
========
class PerfilActivity: AppCompatActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        enableEdgeToEdge()
        setContentView(R.layout.activity_perfil)
>>>>>>>> refs/remotes/origin/Alejandro:Aplicaciones de Moviles/app/app/src/main/java/com/example/filmcast/ui/login/PerfilActivity.kt

    }
}