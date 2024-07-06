from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType


class StrPermisosModelo:
    def __init__(self, clase_modelo):
        self.clase_modelo = clase_modelo
        self.nombre_modelo = None
        self.permiso_add = None
        self.permiso_change = None
        self.permiso_delete = None
        self.permiso_view = None

    def get_lista(self):
        return [
            self.permiso_add,
            self.permiso_change,
            self.permiso_delete,
            self.permiso_view,
        ]


def get_default_model_permissions_full(model) -> StrPermisosModelo:
    """
    Returns a list with the default permission names for a given model class.
    """
    r = StrPermisosModelo(model)
    opts = model._meta
    model_name = opts.model_name

    # Build the permission names
    add_perm_name = "add_{}".format(model_name)
    change_perm_name = "change_{}".format(model_name)
    delete_perm_name = "delete_{}".format(model_name)
    view_perm_name = "view_{}".format(model_name)

    r.nombre_modelo = model_name
    r.permiso_add = add_perm_name
    r.permiso_view = view_perm_name
    r.permiso_change = change_perm_name
    r.permiso_delete = delete_perm_name
    # Return the permissions as a list
    return r


def get_permission_full_name(clase_modelo, nombre_permiso):
    content_type = ContentType.objects.get_for_model(clase_modelo)
    permission = Permission.objects.get(
        codename=nombre_permiso, content_type=content_type
    )
    return permission


def get_permission(clase_modelo, tipo_permiso) -> Permission:
    nombresPermisos = get_default_model_permissions_full(clase_modelo)
    if tipo_permiso == "add":
        nombre_permiso = nombresPermisos.permiso_add
    elif tipo_permiso == "change":
        nombre_permiso = nombresPermisos.permiso_change
    elif tipo_permiso == "delete":
        nombre_permiso = nombresPermisos.permiso_delete
    elif tipo_permiso == "view":
        nombre_permiso = nombresPermisos.permiso_view
    else:
        nombre_permiso = tipo_permiso

    # recuperar el permiso
    content_type = ContentType.objects.get_for_model(clase_modelo)
    permission = Permission.objects.get(
        codename=nombre_permiso, content_type=content_type
    )
    return permission


def create_group_is_necessary_and_set_permissions(nombre_grupo, listaDePermisos):
    new_group, created = Group.objects.get_or_create(name=nombre_grupo)
    # if created:
    for permiso in listaDePermisos:
        new_group.permissions.add(permiso)
    return new_group


def crear_rol(
    nombre_rol,
    lista_modelos=None,
    lista_modelos_solo_update=None,
    lista_modelos_solo_create=None,
    lista_modelos_solo_view=None,
    lista_modelos_solo_delete=None,
):
    if not lista_modelos_solo_delete:
        lista_modelos_solo_delete = []
    if not lista_modelos_solo_create:
        lista_modelos_solo_create = []
    if not lista_modelos_solo_view:
        lista_modelos_solo_view = []

    permisos = []
    for m in lista_modelos:
        # print(f"m {m}")
        str_permisos = get_default_model_permissions_full(m)
        for p in str_permisos.get_lista():
            # try:
            # print(f"m {m} {p}")
            permiso = get_permission_full_name(m, p)
            permisos.append(permiso)
            # except:
            #     print(f"m {m} {p}")
            #     assert False
    tipos_de_permiso = ["change", "view"]
    for m in lista_modelos_solo_update:
        for tipo in tipos_de_permiso:
            permisos.append(get_permission(m, tipo))
    tipos_de_permiso = ["delete", "view"]
    for m in lista_modelos_solo_delete:
        for tipo in tipos_de_permiso:
            permisos.append(get_permission(m, tipo))
    tipos_de_permiso = ["add", "view"]
    for m in lista_modelos_solo_create:
        for tipo in tipos_de_permiso:
            permisos.append(get_permission(m, tipo))
    tipos_de_permiso = ["view"]
    for m in lista_modelos_solo_view:
        for tipo in tipos_de_permiso:
            permisos.append(get_permission(m, tipo))
    create_group_is_necessary_and_set_permissions(nombre_rol, permisos)
