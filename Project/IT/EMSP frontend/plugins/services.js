import AuthService from "@/services/auth";
import BookService from "@/services/book";
import CsService from "@/services/cs";

export default ({ $axios }, inject) => {
  const authService = AuthService($axios);
  const bookService = BookService($axios);
  const csService = CsService($axios);

  inject("services", {
    auth: authService,
    book: bookService,
    cs: csService,
  });
};
