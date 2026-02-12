export const requiredRule = [
    (v: string) => !!v || 'Este campo es requerido.'
]

export const numberRule = [
    (v: string) => {
        const validation = /^[0-9]+$/
        return validation.test(v) || "Este campo debe contener solo números."
    }
]

export const nonNegativeRule = [
    (v: number) => v >= 0 || `Este campo no puede ser negativo.`
]

export const identificacionRule = [
    (v: string) => {
        const errorMessage = 'Cédula invalida';
        let vnTotal = 0;
        const vcCedula = v.replace(/-/g, "");
        const pLongCed = vcCedula.trim().length;
        const digitoMult = [1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1];
    
        if (pLongCed !== 11) {
            return errorMessage;
        }
    
        for (let vDig = 1; vDig <= pLongCed; vDig++) {
            const digito = parseInt(vcCedula.charAt(vDig - 1), 10);
            const vCalculo = digito * digitoMult[vDig - 1]!;
            if (vCalculo < 10) {
                vnTotal += vCalculo;
            } else {
                const [first, second] = vCalculo.toString().split("").map(n => parseInt(n, 10));
                vnTotal += first! + second!;
            }
        }

        console.log(v);
    
        return (vnTotal % 10 === 0) || errorMessage;
    }
]

export const maxLengthRule = (max: number) => [
    (v: string) => v.length === max || `Este campo no debe tener mas de ${max} caracteres.`
]

export const validateList = (list: any[]) => [
    () => list.length > 0 || 'Debe seleccionar al menos un elemento.'
]