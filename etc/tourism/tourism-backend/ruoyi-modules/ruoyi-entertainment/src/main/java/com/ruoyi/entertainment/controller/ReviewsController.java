package com.ruoyi.entertainment.controller;

import java.util.List;
import java.io.IOException;
import javax.servlet.http.HttpServletResponse;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.PutMapping;
import org.springframework.web.bind.annotation.DeleteMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;
import com.ruoyi.common.log.annotation.Log;
import com.ruoyi.common.log.enums.BusinessType;
import com.ruoyi.common.security.annotation.RequiresPermissions;
import com.ruoyi.entertainment.domain.Reviews;
import com.ruoyi.entertainment.service.IReviewsService;
import com.ruoyi.common.core.web.controller.BaseController;
import com.ruoyi.common.core.web.domain.AjaxResult;
import com.ruoyi.common.core.utils.poi.ExcelUtil;
import com.ruoyi.common.core.web.page.TableDataInfo;

/**
 * 餐饮娱乐评价Controller
 * 
 * @author ningf
 * @date 2024-07-15
 */
@RestController
@RequestMapping("/reviews")
public class ReviewsController extends BaseController
{
    @Autowired
    private IReviewsService reviewsService;

    /**
     * 查询餐饮娱乐评价列表
     */
    @GetMapping("/list")
    public TableDataInfo list(Reviews reviews)
    {
        startPage();
        List<Reviews> list = reviewsService.selectReviewsList(reviews);
        return getDataTable(list);
    }

    /**
     * 导出餐饮娱乐评价列表
     */
    @Log(title = "餐饮娱乐评价", businessType = BusinessType.EXPORT)
    @PostMapping("/export")
    public void export(HttpServletResponse response, Reviews reviews)
    {
        List<Reviews> list = reviewsService.selectReviewsList(reviews);
        ExcelUtil<Reviews> util = new ExcelUtil<Reviews>(Reviews.class);
        util.exportExcel(response, list, "餐饮娱乐评价数据");
    }

    /**
     * 获取餐饮娱乐评价详细信息
     */
    @GetMapping(value = "/{id}")
    public AjaxResult getInfo(@PathVariable("id") Long id)
    {
        return success(reviewsService.selectReviewsById(id));
    }

    /**
     * 新增餐饮娱乐评价
     */
    @Log(title = "餐饮娱乐评价", businessType = BusinessType.INSERT)
    @PostMapping
    public AjaxResult add(@RequestBody Reviews reviews)
    {
        return toAjax(reviewsService.insertReviews(reviews));
    }

    /**
     * 修改餐饮娱乐评价
     */
    @Log(title = "餐饮娱乐评价", businessType = BusinessType.UPDATE)
    @PutMapping
    public AjaxResult edit(@RequestBody Reviews reviews)
    {
        return toAjax(reviewsService.updateReviews(reviews));
    }

    /**
     * 删除餐饮娱乐评价
     */
    @Log(title = "餐饮娱乐评价", businessType = BusinessType.DELETE)
	@DeleteMapping("/{ids}")
    public AjaxResult remove(@PathVariable Long[] ids)
    {
        return toAjax(reviewsService.deleteReviewsByIds(ids));
    }
}
