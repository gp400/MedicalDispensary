export const requiredRule = [
    (v: string) => !!v || 'Este campo es requerido.'
]

export const numberRule = [
    (v: string) => {
        const validation = /^[0-9]+$/
        return validation.test(v) || "Este campo debe contener solo números."
    }
]

export const maxLengthRule = (max: number) => [
    (v: string) => v.length === max || `Este campo no debe tener ${max} caracteres.`
]

export const validateList = (list: any[]) => [
    () => list.length > 0 || 'Debe seleccionar al menos un elemento.'
]